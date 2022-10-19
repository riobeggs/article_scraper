import os
import re
import tempfile
import urllib.request

from bs4 import BeautifulSoup
from fpdf import FPDF
from selenium import webdriver


class Article:
    def __init__(self, url: str):

        driver = webdriver.Safari()
        driver.get(url)

        self._html = BeautifulSoup(driver.page_source, "lxml")
        self._article_text = None
        self._article_title = None
        self._text_list = []
        self._article_image = None
        self._cwd = None
        self._tmpdir = None
        self._pdf_name = None

    def _make_tmpdir(self):
        """
        Sets up temporary directory
        """
        self._cwd = os.path.dirname(__file__)

        self._tmpdir = tempfile.TemporaryDirectory(dir=self._cwd)

    def _scrape_title(self):
        """
        Scrapes given url for article title.
        """
        try:
            find_heading = self._html.find(class_="article__heading")
            for heading in find_heading:
                heading = str(heading)
                self._article_title = re.sub(re.compile(r"<.*?>"), "", heading)
                self._article_title = self._article_title.capitalize()
        except:
            pass

    def _scrape_text(self):
        """
        Scrapes given url for article title.
        """
        subscription_text = "$1.99per week Share this article Reminder, this is a Premium article and requires a subscription to read."
        try:
            find_article = self._html.find_all(class_="article__body")
            content = find_article[0].find_all("p")
            for line in content:
                line = str(line)
                text = re.sub(re.compile("<.*?>"), "", line)
                text = text.replace("\n", " ")
                self._text_list.append(text)
            self._article_text = " ".join(self._text_list)
            self._article_text = self._article_text.replace(
                subscription_text, ""
            ).strip()
        except:
            pass

    def _scrape_image(self):
        """
        Scrapes given url for article header image.
        """
        try:
            all_img_tags = self._html.find_all("img")
            img_tags = str(all_img_tags)
            images = img_tags.split(",")
            for image in images:
                if "1440x810" not in image:
                    continue

                pattern = re.compile(r"^.*?\.jpg")
                image_url = pattern.findall(image)

                self._article_image = self._download_image(image_url[0])

                break
        except:
            pass

    def _download_image(self, url) -> str:
        """
        Downloads article header image to tmpdir.
        """
        assert isinstance(
            url, str
        ), f"url is the wrong type, expected string but got {type(url)}"
        self._article_title = re.sub(r"[^a-zA-Z0-9]", "", self._article_title)

        image_file_path = f"{self._tmpdir.name}/{self._article_title}.jpg"
        urllib.request.urlretrieve(url, image_file_path)

        return image_file_path

    def _make_pdf(self) -> str:
        """
        Creates a pdf file containing the chosen article.

        Returns the file name as a string
        """

        pdf = FPDF()

        tnr = "Times New Roman"
        tnrb = "Times New Roman Bold"

        pdf.add_font(tnr, "", f"{self._cwd}/fonts/times new roman.ttf", uni=True)
        pdf.add_font(tnrb, "", f"{self._cwd}/fonts/times new roman bold.ttf", uni=True)
        pdf.set_margins(30, 23, 30)
        pdf.add_page()

        # create title
        if isinstance(self._article_title, str):
            pdf.set_font(tnrb, size=28)
            pdf.multi_cell(150, 12, txt=self._article_title, align="L")

        if isinstance(self._article_image, str):
            # insert image
            pdf.cell(150, 5, ln=2)
            pdf.set_y(pdf.get_y())
            pdf.image(self._article_image, w=(pdf.w - 60))
            pdf.cell(150, 5, ln=2)
        else:
            # insert line break
            pdf.set_font(tnrb, size=28)
            pdf.cell(150, 7, ln=2)

        # create text
        # TODO change to aa font that supports macrons
        if isinstance(self._article_text, str):
            pdf.set_font(tnr, size=12)
            pdf.set_y(pdf.get_y())
            pdf.multi_cell(150, 8, txt=self._article_text, align="L")

        if self._article_title == None:
            self._article_title = "article"

        self._article_title = re.sub(r"[^a-zA-Z0-9]", "", self._article_title)
        self._article_title = self._article_title.replace(" ", "")

        path = f"{self._tmpdir.name}/{self._article_title}.pdf"
        pdf.output(path)

        # returns the file name as a string
        self._pdf_name = f"{self._article_title}.pdf"

    def run(self):
        """
        Runs methods required for gathering article content.
        """
        self._make_tmpdir()
        self._scrape_title()
        self._scrape_text()
        self._scrape_image()
        self._make_pdf()

    @property
    def tmpdir(self):
        return self._tmpdir

    @property
    def pdf_name(self):
        return self._pdf_name