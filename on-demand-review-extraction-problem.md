# On-demand Review Extraction

## Objective

Develop an API server that can extract reviews from specified Amazon or Flipkart product page. The API should automatically detect the site based on the URL, and scrape the reviews, manage pagination to collect all available reviews, and return the data in a structured JSON format.
API service should be capable of handling thousands of requests per day.
Note: Scraper should only accept the urls for the given sites: **Flipkart**, **Amazon**


## Requirements

### 1. API Endpoints

Create an API service that accepts a product page URL as input and returns the extracted reviews. The API should work with Flipkart and Amazon and accurately extract relevant information.

Note: This endpoint is just as an example, you can consider different endpoints as per your design.

- **Example:**
  - **Endpoint:** `POST /extract-reviews`
  - **Input:** JSON containing the product page URL.
  - **Output:** JSON with a list of reviews, including reviewer name, rating, review text, date, and other relevant data.

### 2. Features

- **Pagination Handling:**  
  The API should handle paginated reviews, fetching all available pages until no more reviews are left.

- **Scalability Considerations:**  
  Implement the API to handle large numbers of reviews efficiently. Use timeouts, retries, and rate-limiting to prevent getting blocked by websites.

---

## Programming Language

### Choice of Language

You are welcome to use any programming language for this assignment. Choose the language and tools you are most comfortable and confident with.


## Technical Requirements

### 1. Browser Automation Frameworks
Data extraction can be performed using libraries like:
- **Playwright**
- **Puppeteer**
- **Selenium**
- **BeautifulSoup**
- **Scrapy**

---

## Documentation

### README File
Your submission should include a clear and detailed `README.md` file with:
- A **detailed solution approach** outlining your methodology.
- Diagrams illustrating the system architecture or workflow.
- Instructions on how to set up and run the project.
- Examples demonstrating API usage and sample responses.

---

## Submission

Please submit the following:
- The complete code in a **GitHub repository** (with proper documentation).
- A `README.md` file with setup instructions, dependencies, and how to run the API.
- Email the repository URL to us upon completion.

---

## Evaluation Criteria

### Functionality
- Successfully extracts reviews from any product review page by parsing HTML content.
- Handles pagination and dynamic content accurately.

### Technical Implementation
- Proper integration of browser automation tools to retrieve dynamic or rendered content.

### API Specification Compliance
- Adheres to the provided API endpoint specifications and response format.

### Documentation Quality
- Clear and comprehensive `README.md`.
- Quality of diagrams and explanations.

### Code Quality
- Clean, readable, and well-organized code.
- Appropriate use of version control with clear commit messages.

### Bonus Points
- Easily deployable API code (Using docker compose).
- Easily deployable frontend UI that integrates seamlessly with the API. (Using docker compose)

---

## Hints

### Browser Automation
Use tools like **Playwright**, **Selenium**, or **Puppeteer** for headless browser automation to handle rendered content and user interactions (e.g., clicking, scrolling for pagination).

---

Good luck! We look forward to reviewing your submission.
