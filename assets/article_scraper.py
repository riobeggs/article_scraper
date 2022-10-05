import assets.webdriver as Driver
from bs4 import BeautifulSoup
import re


class Article:
    _html = None
    _article_text = None
    _content = None

    def __init__(self, driver=Driver.run_web_driver()):
        self._driver = driver
        self._html = None
        self._article_text = []
        self._content = None

    def scrape_text(self) -> list:
        self._html = BeautifulSoup(self._driver.page_source, "html.parser")

        # Scrape article text
        article = self._html.find_all(class_="article__body ZSXJFNSWTapB article__content")
        for article_content in article:
            self._content = article_content.find_all("p")
        for line in self._content:
            line = str(line)
            text = re.sub(re.compile('<.*?>'), "", line)
            text = text.replace("\n", " ")
            self._article_text.append(text)
        return self._article_text

    @property
    def article_text(self):
        return " ".join(self._article_text)
