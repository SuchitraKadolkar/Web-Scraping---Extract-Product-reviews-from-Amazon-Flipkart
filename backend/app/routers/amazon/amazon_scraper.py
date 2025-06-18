import asyncio
import random
import logging
# from playwright.async_api import async_playwright
# #from playwright_stealth import stealth_async
# from playwright_stealth.stealth import stealth_async
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
#from commons.constants import USER_DATA_DIR

USER_DATA_DIR = "amazon_session"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class AmazonScraper:
    def __init__(self, url):
        self.url = url
        
    # add explicit delay to avoid detection and throttling by Amazon’s anti-bot systems.
    async def explicit_delay(self, min_sec=2, max_sec=5):
        await asyncio.sleep(random.uniform(min_sec, max_sec))


    async def extract_reviews(self, pageNumber):
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False
            )
            page = browser.pages[0] if browser.pages else await browser.new_page()
            await page.set_extra_http_headers({
                "User-Agent": USER_AGENT
            })
            await stealth_async(page)

            await page.goto(self.url)
            cookies = await page.context.cookies()
            print("Cookies count:", len(cookies))

            await self.explicit_delay()

            # Find 'See more reviews' link and click on that
            try:
                see_all_reviews = page.locator(".a-link-emphasis.a-text-bold").first
                await see_all_reviews.wait_for(state="visible", timeout=10000)
                await see_all_reviews.scroll_into_view_if_needed()
                await see_all_reviews.click()
            except Exception as e:
                logger.error("Failed to click See more reviews:", e)
                browser.close()
                return

            await self.explicit_delay()

            current_url = page.url
            logger.info("Redirected URL:", current_url)

            page_num = 1
            while page_num < int(pageNumber):
                next_button = page.locator("li.a-last a")
                if await next_button.count() == 0:
                    print("No more pages found.")
                    break

                try:
                    await next_button.click()
                    await self.explicit_delay()
                    page_num += 1
                except Exception as e:
                    print("Failed to click next page:", e)
                    break

            await page.wait_for_selector(".review")
            reviews = await page.query_selector_all(".review")
            
            data = []
            for review in reviews:
                name = await review.query_selector(".a-profile-name")
                              
                rating = await review.query_selector(".review-rating span")
                
                date = await review.query_selector(".review-date")
                date_raw = await date.inner_text() if date else "N/A"

                location = "N/A"
                if "Reviewed in" in date_raw:
                    parts = date_raw.split(" on ")
                    if len(parts) == 2:
                        location_part = parts[0].replace("Reviewed in ", "").strip()
                        date_part = parts[1].strip()
                        location = location_part
                        date_raw = date_part

                text = await review.query_selector(".review-text-content span")

                review_data = {
                    "name": await name.inner_text() if name else "N/A",
                    "rating": await rating.inner_text() if rating else "N/A",
                    "comment": await text.inner_text() if text else "N/A",
                    "date": date_raw,
                    "location": location  
                } 

                data.append(review_data)

            await browser.close()
        response = {
            "data": data,
            "page": pageNumber,
            "total_pages": 10
        }
        return response

async def main(url, pageNumber):
    scraper = AmazonScraper(url)
    result = await scraper.extract_reviews(pageNumber)

    print(result)

# Run the async main function
if __name__ == "__main__":
    url = input("Enter valid Amazon product url: ")
    pageNumber = input("Enter page number: ")
    asyncio.run(main(url, pageNumber))
