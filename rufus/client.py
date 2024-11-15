import os
from typing import List, Dict
from dotenv import load_dotenv
from .scraper import WebScraper
from .processor import ContentProcessor

class RufusClient:
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv('RUFUS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set the 'RUFUS_API_KEY' environment variable.")
        self.scraper = WebScraper()
        self.processor = ContentProcessor(api_key=self.api_key)

    def scrape(self, url: str, instructions: str = None) -> List[Dict]:
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with 'http://' or 'https://'.")
        raw_content = self.scraper.crawl(url)
        return self.processor.process(raw_content, instructions)
