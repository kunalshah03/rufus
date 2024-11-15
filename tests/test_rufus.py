import unittest
from rufus import RufusClient

class TestRufus(unittest.TestCase):
    def setUp(self):
        self.client = RufusClient()

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            self.client.scrape("invalid-url")

    def test_scraping(self):
        docs = self.client.scrape(
            "https://example.com",
            instructions="Find product information"
        )
        self.assertIsInstance(docs, list)
        if docs:
            self.assertIn('title', docs[0])
            self.assertIn('summary', docs[0])
            self.assertIn('metadata', docs[0])

if __name__ == '__main__':
    unittest.main()
