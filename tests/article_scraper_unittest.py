import logging
import unittest

from assets.article_scraper import Article
from requests.exceptions import MissingSchema


class ArticleScraper(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.debug(f"Setting Up - {self._testMethodName}")

        self._exampleURL = "https://tinyurl.com/mms6y95d"
        self.scraper = Article(self._exampleURL)

        return super().setUp()

    def tearDown(self) -> None:
        self.logger.debug("Tearing Down")

        if self.scraper.tmpdir is not None:
            self.scraper.tmpdir.cleanup()

        return super().tearDown()

    def test_init_loads_url(self):
        """
        Pass in a url and check that it loads.
        """
        scraper = Article(self._exampleURL)

        self.assertIsInstance(scraper._url, int)
        self.assertIsInstance(scraper._cwd, int)

        self.assertIsNone(scraper._html)
        self.assertIsNone(scraper._html_parser)
        self.assertIsNone(scraper._tmpdir)
        self.assertIsNone(scraper._article_title)
        self.assertIsNone(scraper._article_text)
        self.assertIsNone(scraper._article_image)
        self.assertIsNone(scraper._image_url)
        self.assertIsNone(scraper._pdf_name)

    def test_init_loads_invalid_url(self):
        """
        Tests that an invalid url passed in throws an error.
        """
        # Arrange
        expected_error_msg = "Invalid URL 'invalid_url': No scheme supplied. Perhaps you meant http://invalid_url?"

        # Act
        with self.assertRaises(MissingSchema) as error_context:
            self.scraper._url = "invalid_url"
            self.scraper._get_html()

        actual_error_msg = str(error_context.exception)

        # Assert
        self.assertEqual(actual_error_msg, expected_error_msg)

    def test_tmpdir(self):
        """
        Test that a temporary directory has been created.
        """
        # Act
        self.scraper._make_tmpdir()

        # Assert
        self.assertIsInstance(self.scraper.tmpdir.name, str)

    def test_scrape_title(self):
        """
        Scrape the title from our test asset and assert that its working as intended.
        """
        # Arrange
        expected_title = (
            "Fulton Hogan staff take up shares as dividend jumps 46 per cent"
        )
        self.scraper._parse_html()

        # Act
        self.scraper._scrape_title()

        # Assert
        self.assertEqual(self.scraper.title, expected_title)

    def test_scrape_text(self):
        """
        Scrape the text from our test asset and assert that its working as intended.
        """
        # Arrange
        self.scraper._parse_html()

        # Act
        self.scraper._scrape_text()

        # Assert
        self.assertIsInstance(self.scraper.text, str)

    def test_scrape_image(self):
        """
        Scrape the image from our test asset and assert that its working as intended.
        """
        # Arrange
        self.scraper._parse_html()
        self.scraper._make_tmpdir()
        self.scraper._scrape_title()

        # Act
        self.scraper._scrape_image()

        # Assert
        self.assertIsInstance(self.scraper.image, str)

    def test_pdf_maker(self):
        """
        Assert a pdf has been created.
        """
        # Act
        self.scraper.run()

        # Assert
        self.assertIsInstance(self.scraper.pdf_name, str)


if __name__ == "__main__":
    unittest.main()
