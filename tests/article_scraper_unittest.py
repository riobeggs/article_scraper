import logging
import unittest

from bs4 import BeautifulSoup
from selenium.common.exceptions import InvalidArgumentException

from assets.article_scraper import Article


class ArticleScraper(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        self.logger.addHandler(consoleHandler)

        self.logger.debug(f"Setting Up - {self._testMethodName}")

        self._exampleURL = "https://tinyurl.com/mms6y95d"
        self.scraper = Article(self._exampleURL)

        return super().setUp()

    def tearDown(self) -> None:
        self.logger.debug("Tearing Down")
        return super().tearDown()

    def test_init_loads_url(self):
        """
        Pass in a url and check that it loads.
        """
        self.assertIsInstance(self.scraper._html, BeautifulSoup)
        self.assertIsNone(self.scraper._article_title)
        self.assertIsNone(self.scraper._article_text)
        self.assertIsNone(self.scraper._article_image)
        self.assertIsNone(self.scraper._cwd)
        self.assertIsNone(self.scraper._image_url)
        self.assertIsNone(self.scraper._tmpdir)
        self.assertIsNone(self.scraper._pdf_name)

    def test_init_loads_invalid_url(self):
        """
        Tests that an invalid url passed in throws an error.
        """
        with self.assertRaises(InvalidArgumentException) as error_context:
            _ = Article("invalid_url")

        actual_error_msg = str(error_context.exception)
        expected_error_msg = "Message: Could not parse requested URL 'invalid_url'\n"

        self.assertEqual(actual_error_msg, expected_error_msg)

    def test_tmpdir(self):
        """
        Test that a temporary directory has been created.
        """
        # Act
        self.scraper._make_tmpdir()

        # Assert
        self.assertIsInstance(self.scraper.tmpdir.name, str)
        self.scraper.tmpdir.cleanup()

    def test_scrape_title(self):
        """
        Scrape the title from our test asset and assert that its working as intended
        """
        # Arrange
        expected_title = (
            "Fulton Hogan staff take up shares as dividend jumps 46 per cent"
        )

        # Act
        self.scraper._scrape_title()
        actual_title = self.scraper.title

        # Assert
        self.assertEqual(actual_title, expected_title)

    def test_scrape_text(self):
        """
        Scrape the text from our test asset and assert that its working as intended
        """
        # Act
        self.scraper._scrape_text()

        # Assert
        self.assertIsInstance(self.scraper.text, str)

    def test_scrape_image(self):
        """
        Scrape the image from our test asset and assert that its working as intended        
        """
        # Arrange
        self.scraper._make_tmpdir()
        self.scraper._scrape_title()
        self.scraper._scrape_text()

        # Act
        self.scraper._scrape_image_url()

        # Assert
        self.assertIsInstance(self.scraper.image, str)
        self.scraper.tmpdir.cleanup()


if __name__ == "__main__":
    unittest.main()
