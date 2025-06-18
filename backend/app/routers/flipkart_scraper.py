from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from constants.constants import *
import time
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class FlipkartScrapper:
    def __init__(self, url):
        self.url = url
 
    def extract_reviews(self, pageNumber):
        # Setup Chrome Options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # Required for Docker
        

        # Use correct path to chromedriver installed in Docker
        service = Service('/usr/bin/chromedriver')

        # Setup ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)

        # Open URL in browser
        driver.get(self.url)
        time.sleep(4)

        try:
            # Check if reviews are exists
            web_page = requests.get(self.url)

            # Parse the HTML content
            soup = BeautifulSoup(web_page.content, 'html.parser')

            # If page contains text as "Be the first to Review this product"
            # then we should return proper message as no reviews exists for a product
            element = soup.find('span', class_=REVIEW_ELEMENT)
            if element:
                logger.info("No reviews exists for this product.")
                response = {
                    "data": "No reviews exists for this product. Try searching for other product.",
                    "page": 1,
                    "total_pages": 1
                }
                return response
        
            customer_ratings = []
            customer_comments = []
            customer_names = []
            customer_dates = []
            customer_locations = []
            reviews = []

            all_reviews_button = driver.find_element(By.CLASS_NAME, ALL_REVIEW_BUTTON_ELEMENT) 
            all_reviews_button.click()
            current_url = driver.current_url
            logger.info("Redirected URL:", current_url)
            time.sleep(4)

            web_page = requests.get(current_url)

            # Parse the HTML content
            soup = BeautifulSoup(web_page.content, 'html.parser')

            # Get count of total number of review pages
            pages_tag = soup.select_one(PAGE_COUNT_ELEMENT)

            if pages_tag:
                span_tag = pages_tag.find('span')
                if span_tag:
                    # search for page number count string
                    total_pages = span_tag.text.split()[-1]
                    logger.info("Page count text:", total_pages)
                else:
                    logger.error("Unable to fetch total number of pages")
            else:
                logger.info("This product has only single page review.")
                total_pages = 1

          
            pagination_url = current_url + "&page=" + str(pageNumber)
            web_page = requests.get(pagination_url)

            # Parse the HTML content
            soup = BeautifulSoup(web_page.content, 'html.parser')

            # Extract customer ratings
            ratings = soup.find_all('div', class_=RATING_ELEMENT)
            # Extract customer review comments
            comments = soup.find_all('div', class_=COMMENT_ELEMENT) 
            # Extract customer names and review dates
            names_and_dates = soup.find_all('p', class_=NAME_DATE_ELEMENT)
            # Extract customer location
            parent_tags = soup.find_all('p', class_=LOCATION_ELEMENT)
            for tag in parent_tags:
                if tag:
                    spans = tag.find_all('span')
                    if len(spans) >= 2:
                        customer_locations.append(spans[1].text.lstrip(", ").strip())

            # Close driver
            driver.quit()


            for i in range(1, len(ratings)):
                customer_ratings.append(ratings[i].get_text())
            for c in comments:
                customer_comments.append(c.get_text())

            for i in range(0, len(names_and_dates)-1, 2):
                customer_names.append(names_and_dates[i].get_text())
                customer_dates.append(names_and_dates[i+1].get_text())
                                                
            # Assuming all reviews have all the below fields i.e name, rating, comment etc.
            for i in range(len(customer_names)):
                review = {
                    "name": customer_names[i],
                    "rating": customer_ratings[i],
                    "comment": customer_comments[i],
                    "date": customer_dates[i],
                    "location": customer_locations[i]
                }
                reviews.append(review) 
            
            response = {
                "data": reviews,
                "page": pageNumber,
                "total_pages": int(total_pages)
            }
            return response

        except Exception as e:
            logger.error("Caught exception: ", e)
            driver.quit()
            return {"message": 'Oops! Something went wrong.'}
