
class AmazonScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Use your own user agent',
            'Accept-Language': 'en-us,en;q=0.5'
        }

    def extract_reviews(self, pageNumber):
        pass
