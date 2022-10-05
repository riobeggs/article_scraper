import assets.webdriver as Driver
from bs4 import BeautifulSoup
import re


class Article:
    _html = None
    _article_text = None
    _text_list = None

    def __init__(self, driver=Driver.run_web_driver()):
        self._driver = driver
        self._html = None
        self._article_text = None
        self._text_list = []

    def scrape_text(self) -> list:
        self._html = BeautifulSoup(self._driver.page_source, "html.parser")
        subscription_text = "$1.99per week Share this article Reminder, this is a Premium article and requires a subscription to read."

        # Scrape article text
        article = self._html.find_all(class_="article__body")
        content = article[0].find_all("p")
        for line in content:
            line = str(line)
            text = re.sub(re.compile("<.*?>"), "", line)
            text = text.replace("\n", " ")
            self._text_list.append(text)
        self._article_text = " ".join(self._text_list)
        self._article_text = self._article_text.replace(subscription_text, "").strip()
        return self._article_text

    @property
    def article_text(self):
        return self._article_text
