from assets.image_downloader import download_image
import assets.webdriver as Driver
from bs4 import BeautifulSoup
import re


class Article:
    _driver = None
    _html = None
    _article_text = None
    _article_title = None
    _text_list = None
    _article_image = None

    def __init__(self, driver=Driver.run_web_driver()):
        self._driver = driver
        self._html = BeautifulSoup(self._driver.page_source, "html.parser")
        self._article_text = None
        self._article_title = None
        self._text_list = []
        self._article_image = None

    def scrape_title(self) -> str:
        """
        Scrapes given url for article title.

        Returns article title as a string.
        """
        find_heading = self._html.find(class_="article__heading")
        for heading in find_heading:
            heading = str(heading)
            self._article_title = re.sub(re.compile("<.*?>"), "", heading)
            self._article_title = self._article_title.capitalize()
        return self._article_title

    def scrape_text(self) -> str:
        """
        Scrapes given url for article title.

        Returns article title as a string.
        """
        subscription_text = "$1.99per week Share this article Reminder, this is a Premium article and requires a subscription to read."
        find_article = self._html.find_all(class_="article__body")
        content = find_article[0].find_all("p")
        for line in content:
            line = str(line)
            text = re.sub(re.compile("<.*?>"), "", line)
            text = text.replace("\n", " ")
            self._text_list.append(text)
        self._article_text = " ".join(self._text_list)
        self._article_text = self._article_text.replace(subscription_text, "").strip()
        return self._article_text

    def scrape_image(self) -> str | None:
        images = self._html.find_all("img")
        for image in images:
            if "www.nzherald.co.nz" in image:
                if "1440x810" in image:
                    self._article_image = download_image(self._article_title, image["src"])
                    return self._article_image


    @property
    def article_title(self):
        return self._article_title

    @property
    def article_text(self):
        return self._article_text

    @property
    def article_image(self):
        return self._article_image
