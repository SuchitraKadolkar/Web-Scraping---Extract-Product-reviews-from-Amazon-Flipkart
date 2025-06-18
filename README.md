# Web-Scraping---Extract-Product-reviews-from-Amazon-Flipkart

# Flipkart & Amazon Review Scraper

This is a small web application developed to extract customer reviews from a specified Flipkart or Amazon product page using web scraping tools like Selenium, BeautifulSoup, and Playwright. It features a FastAPI backend, a simple HTML/JavaScript frontend, and is deployed using Docker containers.

---

## Goals

1. Automatically extract product reviews (name, rating, comment, date, location) from Flipkart or Amazon.
2. Support pagination to access reviews across multiple pages.
3. Provide a RESTful API and an easy-to-use web interface.
4. Route all incoming requests via FastAPI backend.
5. Automatically detect the platform (Flipkart/Amazon) based on the input URL.
6. Perform headless scraping within Docker containers.
7. Enable navigation between pages using Previous/Next buttons in the frontend.
8. Display extracted reviews on a dynamic HTML page.

---

## Tech Stack & Methodology

* The backend simulates browser interactions to click on "All reviews" or similar links and extract data from multiple paginated pages.

**Flipkart**: Selenium + BeautifulSoup

**Amazon**: Playwright (requires login session)

---

## Project Directory Structure

```
├── backend/
│   ├── app/
│   │   ├── constants/
│   │   │   └── constants.py
│   │   ├── routers/
│   │   │   ├── amazon/
│   │   │   │   ├── requirements.txt
│   │   │   │   ├── setup.sh
│   │   │   │   ├── amazon_login.py
│   │   │   │   └── amazon_scraper.py
│   │   │   └── flipkart_scraper.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
│
└── docker-compose.yml
```

---

## Solution Approach

### Flipkart Scraping Workflow

1. The user provides a Flipkart product URL through the HTML form.
2. The backend appends the page number (default is 1) to support pagination.
3. It detects whether the URL is from Flipkart or Amazon.
4. Opens the product URL in a Selenium-driven browser.
5. Searches for and clicks on the "All Reviews" link.
6. Constructs the paginated review URL, such as:

   ```
   https://www.flipkart.com/fossil-machine-analog-watch-men/product-reviews/itmeg9efbhqazq6s?pid=WATEG9EFHDYXH83N&lid=LSTWATEG9EFHDYXH83N1FH0F7&marketplace=FLIPKART&page=2
   ```

````
7. Parses the review page using BeautifulSoup to extract the total number of review pages.
8. Extracts each review's details (name, rating, date, comment, location) from the HTML elements.
9. Returns a JSON response with reviews, total pages, and the current page number.
10. Displays the data dynamically in the web UI.

### Setup Instructions (Flipkart)

**Pre-requisites:**
- Docker & Docker Compose installed
- Internet access to install dependencies

**Steps:**
```bash
git clone https://github.com/SuchitraKadolkar/Web-Scraping---Extract-Product-reviews-from-Amazon-Flipkart.git
cd https://github.com/SuchitraKadolkar/Web-Scraping---Extract-Product-reviews-from-Amazon-Flipkart.git
docker-compose up 
````

**Access:**

* Frontend UI: [http://localhost:8080](http://localhost:8080)
* Backend API: [http://localhost:9000/api/extract-reviews](http://localhost:9000/api/extract-reviews)

---

### Amazon Scraping Workflow

1. Amazon requires a logged-in session to avoid CAPTCHA and anti-bot mechanisms.
2. Save a session using Playwright with `headless=False`.
3. Accept product URL and page number via terminal.
4. Open the product page in a Playwright-controlled browser.
5. Locate and click the "See more reviews" link.
6. Click on Next page button until we match provided page number.

   ```
   https://www.amazon.com/product-reviews/B0B4PQDFCL/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
   ```

````
7. Use Playwright selectors to extract review data from each page.
8. Return the data in JSON format.

### Setup Instructions (Amazon)

**Pre-requisites:**
- Python 3.13.x installed
- Internet access for dependency installation

**Steps:**
```bash
cd backend/app/routers/amazon
./setup.sh  # It will install necessary packages

# Save Amazon login session
python amazon_login.py  # Manually log in, then press Enter to save session

# Start review extraction
python amazon_scraper.py  # Enter URL and page number when prompted
````

---

## Limitations

1. Amazon limits the visible reviews on the website to 10 pages.

   * To access all reviews, consider using the official Amazon Product Advertising API.
2. Amazon enforces strong anti-bot mechanisms.

   * Headless scraping may not always respect persistent sessions. It's recommended to use `headless=False` mode during login and scraping.

---

## Notes

* The system detects the e-commerce platform dynamically from the input URL.
* Docker ensures consistent environment setup and isolated dependencies.
* The frontend is intentionally kept simple for ease of integration and testing.

---

## Example URLs

* **Flipkart**:
  `https://www.flipkart.com/fossil-machine-analog-watch-men/p/itmeg9efbhqazq6s?pid=WATEG9EFHDYXH83N&fm=organic&ppt=dynamic&ppn=dynamic&ssid=20vfm1am740000001750224552155`

Sample output:
{
  "success": true,
  "content": {
    "data": [
      {
        "name": "Visakh Chandran",
        "rating": "5",
        "comment": "Go for it without a second thought. It's so premium stylish good looking watch.. Adoring black 🖤",
        "date": "Jun, 2018",
        "location": "Thiruvananthapuram"
      },
      {
        "name": "Uttaron Baruah",
        "rating": "5",
        "comment": "very slick. awesome product, but please do not go by the product image, check the uploaded images. The radium really fires up when exposed to sunlight. it is Litt.",
        "date": "Dec, 2018",
        "location": "Bengaluru"
      },
      {
        "name": "Flipkart Customer",
        "rating": "5",
        "comment": "looks great and feels awesome.... it's quite noticeable.... goes with every dress and every occasion.... the belt quality is really good... must buy at this range price !",
        "date": "Jan, 2019",
        "location": "Pune"
      },
      {
        "name": "Chagamreddy  Bharat kumar",
        "rating": "5",
        "comment": "one word go for it got it for 5500 best price u ever getloving it already love u flipkart",
        "date": "Jan, 2020",
        "location": "Vijayawada"
      },
      {
        "name": "flipkart cusme",
        "rating": "5",
        "comment": "I took first tym Fossil watch my experience is excellent .",
        "date": "Oct, 2019",
        "location": "Bangalore"
      },
      {
        "name": "Kiran bose",
        "rating": "5",
        "comment": "Got this delivered in a day. Its original fossil. This is available at Rs. 7995 across all sites. But this seller gives it for around 6. Night visibility is less like in all fossils. Overall it's worth the price. Its all black. The dial is not grey like in the picture. Its pure black and it is definitely better than gray dial. The chronograph needles are blue. Main needles are white. I loved it.",
        "date": "Oct, 2017",
        "location": "Bengaluru"
      },
      {
        "name": "ravi arya",
        "rating": "5",
        "comment": "Looks very premium even looking better than a 25k Armani watch",
        "date": "Jan, 2024",
        "location": "Shahjahanpur"
      },
      {
        "name": "Vinu Dominic",
        "rating": "5",
        "comment": "Fantastic one really like it👌👌👌👌",
        "date": "Jan, 2024",
        "location": "Thiruvananthapuram District"
      },
      {
        "name": "Flipkart Customer",
        "rating": "3",
        "comment": "still unsure if the product is unsure after 4-6 months of usage. the date always lags when the month changes. time also has to be adjusted every 3-5 months as the minute hand starts to slow down.",
        "date": "Jul, 2019",
        "location": "Gurugram"
      },
      {
        "name": "DRISHYA  SREEMUKUNTHAN ",
        "rating": "5",
        "comment": "Superbb product. Classyyy lookk",
        "date": "4 months ago",
        "location": "Adoor"
      }
    ],
    "page": 1,
    "total_pages": 2
  }
}
* **Amazon**:
  `https://www.amazon.com/Instant-Pot-Electric-Multi-Cooker-Pressure/dp/B0B4PQDFCL/ref=cm_cr_arp_d_product_top?ie=UTF8`

  Sample output:

  {'data': [{'name': 'Yusleidy Carrazana', 'rating': '5.0 out of 5 stars', 'comment': 'Esta olla ha cumplido mis expectativas es realmente muy funcional estoy muy contenta con la compra', 'date': 'April 5, 2025', 'location': 'the United States'}, {'name': 'Kayla', 'rating': '5.0 out of 5 stars', 'comment': 'This is in my opinion better than the instant pot in many ways 1. It gives you a clear progression bar - never have to guess which stage it in! 2. It gives so many convenient preset programs 3. It lets you control the temperature and the pressure and the timer. 4. It is easy to clean and the pressure release is safe and effective.', 'date': 'February 23, 2025', 'location': 'the United States'}, {'name': 'D. Allen', 'rating': '4.0 out of 5 stars', 'comment': "It's a great product but the instructions are very vague. There was a big part about putting in the seal ring with several photos - I tore the box apart looking for it until I realized that it came already installed. Then the part about sealing it and having it build pressure was about two sentences long and I wasn't even sure if it was working right. The tip about turning off the Stay Warm features was an afterthought at the back of the pamphlet but that's a critical thing to know when you can't figure out why it's not cooking!\n\nUsually any type of cooking appliance comes with a recipe book, but none here! Fortunately there are TONS of recipes online that are very easy to follow. And it was in the beef stew recipe I found that they explained what the Stay Warm setting was, how to turn it off, and how to release the pressure when the cooking is done.\n\nLOTS of trial and error to get it cooking the first time. I should have looked up a few Youtube videos. And FYI, the stew was great!", 'date': 'January 4, 2024', 'location': 'the United States'}, {'name': 'Kate H.', 'rating': '5.0 out of 5 stars', 'comment': 'I am an 84 year old Great Grandmother. I just ordered the insta pot because my 87 year old brother has one and loves it. So far I have only used it about four times and I am very pleased with how well it works. The food is delicious and cooked to perfection! I highly recommend it to everyone who loves cooking.', 'date': 'February 22, 2025', 'location': 'the United States'}, {'name': 'Pickle', 'rating': '5.0 out of 5 stars', 'comment': 'I really like this Instant Pot. It is the perfect size for us. The biggest plus is you don’t have to worry about scratching up the inner liner with utensils that are not wooden or silicone.\nI previously had a difficult brand but prefer this one because it has more preprogrammed buttons.', 'date': 'February 24, 2025', 'location': 'the United States'}, {'name': 'theonlysong', 'rating': '3.0 out of 5 stars', 'comment': "Wondering why the company made the sounds on this so soft, I can barely hear them from the other room, especially if I'm watching TV or listening to music while it's cooking.\n\nOver cooked the first thing I made because the alarm was so soft compared to my old instant pot.", 'date': 'March 20, 2025', 'location': 'the United States'}, {'name': 'Moriah Leech', 'rating': '5.0 out of 5 stars', 'comment': 'We got one of these for a wedding gift in 2020 and it recently was violently murdered by a cat who shoved it off the counter. Thankfully we were able to get this replacement and are pleasantly surprised by the updates that have happened in the last 5 years! Looks better and operates just as easily. We use this for cooking chicken straight out of the freezer, and it only takes about 25 minutes to have it ready and we can then add any sauce and shred it!', 'date': 'January 13, 2025', 'location': 'the United States'}, {'name': 'Darren U.', 'rating': '3.0 out of 5 stars', 'comment': '2.5/5. That 3 up there is generous.\n\nThis Instant Pot Duo V6 (emphasis on the V6, it\'s so new that there aren\'t even proper reviews for it yet) was my first ever pressure cooker. I was drawn to the slimmer design and the cheaper price. It seemed like a good bang for the buck. And, it probably is.\n\nThe problem is that a nip and tuck doesn\'t unstick a float valve, which has seemed to be a common problem since Instant Pot inception. I\'m not talking about the vent/seal knob. That\'s fine. I\'m talking about the small metal valve next to the float valve.\n\nThe Instant Pot instructions will tell you to do a water test to make sure everything is fine. 3 cups of water, vent knob to seal, 10 minutes of pressure, quick release and go. My float valve popped up clean as a whistle. Which was supposed to happen, because it was new. But ultimately this was misleading. It\'s not a sufficient context of use. You know what is? Cooking actual food.\n\nSo I\'ve cooked pasta and beans, a brothy Korean soup, alfredo fettuccine, a second water test, and a chunky chicken soup. Not once did the float valve pop up and seal the device by itself, other than the two water tests. Steam came out in plumes and plumes from it, for over 2 minutes. The veggies in the soups were mushy, and the two pasta dishes were charred to the bottom of the pot. It didn\'t even deliver a burn warning; it was still "pre-heating"! Cue the scrubbing. I didn\'t bother trying to press the sides of the lid down to help it seal, because why should I? It\'s 2023. It\'s electric. It should seal by itself -- but didn\'t.\n\nI have returned this Duo V6 and will purchase an Instant Pot Pro. I hope to god that valve is slipperier than an eel, or I\'m just buying a Dutch oven and a sous vide circulator.', 'date': 'March 14, 2023', 'location': 'the United States'}, {'name': 'Mauro Rodriguez', 'rating': '3.0 out of 5 stars', 'comment': 'Todo muy bien… solo llego sin el cable para conectarla', 'date': 'April 22, 2025', 'location': 'the United States'}, {'name': 'MKG', 'rating': '5.0 out of 5 stars', 'comment': 'Love love love. I use almost daily and my only complaint is I wish I could find a proper storage cover for it.', 'date': 'March 21, 2025', 'location': 'the United States'}], 'page': '3', 'total_pages': 10}


