import logging
import os
import sys
import unittest

from bs4 import BeautifulSoup
from selenium.common.exceptions import InvalidArgumentException

sys.path.append(os.path.abspath("."))
from assets.article_scraper import Article

logging.basicConfig(level=logging.DEBUG)


class ArticleScraper(unittest.TestCase):
    def setUp(self) -> None:
        logging.debug(f"Setting Up - {self._testMethodName}")
        self._exampleURL = "https://tinyurl.com/mms6y95d"
        self.scraper = Article(url=self._exampleURL)
        return super().setUp()

    def tearDown(self) -> None:
        logging.debug("Tearing Down")
        return super().tearDown()

    def test_init_loads_url(self):
        """
        Pass in a url and check that it loads.
        """
        self.assertIsInstance(self.scraper._html, BeautifulSoup)
        self.assertIsNone(self.scraper._article_text)
        self.assertIsNone(self.scraper._article_title)
        self.assertIsInstance(self.scraper._text_list, list)
        self.assertIsNone(self.scraper._article_image)
        self.assertIsNone(self.scraper._cwd)
        self.assertIsNone(self.scraper._tmpdir)
        self.assertIsNone(self.scraper._pdf_name)

    def test_init_loads_invalid_url(self):
        """
        Tests that an invalid url passed in throws an error.
        """
        # TODO: Does not work for some reason
        with self.assertRaises(InvalidArgumentException) as error_context:
            self.scraper = Article("invalid_url")

            actual_error_msg = str(error_context.exception)
            expected_error_msg = "Could not parse requested URL 'invalid_url'"

            self.assertEqual(actual_error_msg, expected_error_msg)


if __name__ == "__main__":
    unittest.main()
