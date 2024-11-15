import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List
import asyncio
import aiohttp
import logging
import json
from playwright.async_api import async_playwright

class WebScraper:
   def __init__(self):
       self.visited_urls: Set[str] = set()
       self.max_depth = 3
       self.max_pages = 100
       self.timeout = 30
       self.max_concurrent = 5
       self.headers = {
           'User-Agent': 'Rufus Bot 0.1'
       }

   async def fetch_with_playwright(self, url: str):
       try:
           async with async_playwright() as p:
               browser = await p.chromium.launch()
               page = await browser.new_page()
               await page.goto(url, wait_until='networkidle')
               content = await page.content()
               await browser.close()
               return content
       except Exception as e:
           logging.error(f"Playwright error: {str(e)}")
           return None

   async def fetch_page(self, url: str, session: aiohttp.ClientSession) -> Dict:
    try:
            async with session.get(url, headers=self.headers, timeout=self.timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Basic content extraction
                    text_content = soup.get_text(separator=' ', strip=True)
                    if not text_content:
                        return None

                    return {
                        'url': url,
                        'title': soup.title.string if soup.title else '',
                        'content': text_content,
                        'links': [
                            urljoin(url, link.get('href'))
                            for link in soup.find_all('a', href=True)
                        ]
                    }
                else:
                    logging.error(f"HTTP {response.status} for {url}")
                    return None
    except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

   def should_crawl(self, url: str, base_domain: str) -> bool:
       if url in self.visited_urls:
           return False

       try:
           parsed = urlparse(url)
           if parsed.netloc != base_domain:
               return False

           skip_extensions = ('.pdf', '.jpg', '.png', '.gif', '.css', '.js')
           return not any(url.lower().endswith(ext) for ext in skip_extensions)

       except:
           return False

   async def crawl_async(self, start_url: str) -> List[Dict]:
       base_domain = urlparse(start_url).netloc
       to_visit = {start_url}
       results = []

       connector = aiohttp.TCPConnector(limit=self.max_concurrent)
       timeout = aiohttp.ClientTimeout(total=self.timeout)

       async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
           while to_visit and len(self.visited_urls) < self.max_pages:
               current_batch = list(to_visit)[:self.max_concurrent]
               to_visit = set(list(to_visit)[self.max_concurrent:])

               tasks = [
                   self.fetch_page(url, session)
                   for url in current_batch
                   if self.should_crawl(url, base_domain)
               ]

               pages = await asyncio.gather(*tasks, return_exceptions=True)

               for page in pages:
                   if isinstance(page, dict):
                       self.visited_urls.add(page['url'])
                       results.append(page)
                       for link in page.get('links', []):
                           if self.should_crawl(link, base_domain):
                               to_visit.add(link)

       return results

   def crawl(self, url: str) -> List[Dict]:
       """Main entry point for crawling."""
       return asyncio.run(self.crawl_async(url))
