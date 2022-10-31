import logging
import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath("."))
from assets.article_scraper import Article

logging.basicConfig(level=logging.DEBUG)


class ArticleScraper(unittest.TestCase):
    def setUp(self) -> None:
        logging.debug(f"Setting Up - {self._testMethodName}")
        self.scraper = Article()
        return super().setUp()

    def tearDown(self) -> None:
        logging.debug("Tearing Down")
        return super().tearDown()

    def test_init(self):
        """
        Pass in a file path and check that it loads files.
        """
        self.assertIsInstance(self.scraper._html, BeautifulSoup)
        self.assertIsNone(self.scraper._article_text)
        self.assertIsNone(self.scraper._article_title)
        self.assertIsInstance(self.scraper._text_list, list)
        self.assertIsNone(self.scraper._article_image)
        self.assertIsNone(self.scraper._cwd)
        self.assertIsNone(self.scraper._tmpdir)
        self.assertIsNone(self.scraper._pdf_name)


if __name__ == "__main__":
    unittest.main()
