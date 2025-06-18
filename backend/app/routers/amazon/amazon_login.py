import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = "amazon_session"

async def first_time_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False
        )
        page = await browser.new_page()

        # Open Amazon home page (or any product page directly)
        await page.goto("https://www.amazon.com/")

        print("Please manually login to Amazon in the browser window.")
        print("After login is complete, press Enter here to continue...")
        input()

        await browser.close()

asyncio.run(first_time_login())
