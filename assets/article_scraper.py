from assets.image_downloader import download_image
from bs4 import BeautifulSoup
import wget
import re


class Article:
    _html = None
    _article_text = None
    _article_title = None
    _text_list = None
    _article_image = None

    def __init__(self):

        url = input("Enter URL: ")
        file = wget.download(url, "./assets/html/article.html")
        file = open("./assets/html/article.html")

        self._html = BeautifulSoup(file, "lxml")
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
            image = str(image)
            if "1440" not in image:
                continue

            header_images = image.split(",")

            for image_url in header_images:
                if "1440x" not in image_url:
                    continue
                image_pattern = re.compile(r"^.*?\.jpg")
                image_url = image_pattern.findall(image_url)
                self._article_image = download_image(self._article_title, image_url[0])
                break
            break

    @property
    def article_title(self):
        if not self._article_title:
            self.scrape_title()

        return self._article_title

    @property
    def article_text(self):
        if not self._article_text:
            self.scrape_text()

        return self._article_text

    @property
    def article_image(self):
        if not self._article_image:
            self.scrape_image()

        return self._article_image
