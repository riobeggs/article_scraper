import os
import re
import tempfile
import urllib.request

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


class Article:
    def __init__(self, url: str):
        self._url = url
        self._cwd = os.path.dirname(__file__)

        self._html = None
        self._html_parser = None
        self._tmpdir = None
        self._article_title = None
        self._article_text = None
        self._article_image = None
        self._image_url = None
        self._pdf_name = None

    def _get_html(self):
        """
        Makes a request to the url and retrieves the html as a str.
        """
        self._html = (requests.get(self._url).content).decode("utf-8")

    def _parse_html(self):
        """
        Parses html into a Beautifulsoup object.
        """
        if self._html is None:
            self._get_html()

        self._html_parser = BeautifulSoup(self._html, "html.parser")

    def _make_tmpdir(self):
        """
        Sets up temporary directory.
        """
        self._tmpdir = tempfile.TemporaryDirectory(dir=self._cwd)

    def _scrape_title(self):
        """
        Scrapes given url for article title.
        """
        find_heading = self._html_parser.find(class_="article__heading")

        if find_heading is None:
            find_heading = self._html_parser.find(
                class_="article-bigread__heading__link"
            )

        for heading in find_heading:
            self._article_title = heading

    def _scrape_text(self):
        """
        Scrapes given url for article title.
        """
        subscription_text = "$1.99per week Share this article Reminder, this is a Premium article and requires a subscription to read."
        text_list = []

        find_article = self._html_parser.find_all(class_="article__body")
        content = find_article[0].find_all("p")

        for line in content:
            line = str(line)
            text = re.sub(re.compile("<.*?>"), "", line)
            text = text.replace("\n", " ")
            text_list.append(text)

        self._article_text = " ".join(text_list)
        self._article_text = self._article_text.replace(subscription_text, "").strip()

    def _scrape_image(self):
        """
        Scrapes given url for article header image.
        """
        script = self._html_parser.find_all("script", type="application/javascript")
        script = str(script)
        data_list = script.split(",")

        for image in data_list:
            if "1440x810" in image:
                patterns = (re.compile(r"^.*?\.jpg"), re.compile(r"^.*?\.JPG"))
                for pattern in patterns:
                    url = pattern.findall(image)

                    if len(url) != 0:
                        self._image_url = url[0]
                        self._download_image()

    def _download_image(self) -> str:
        """
        Downloads article header image to tmpdir.
        """
        article_title = re.sub(r"[^a-zA-Z0-9]", "", self._article_title)

        image_file_path = f"{self._tmpdir.name}/{article_title}.jpg"
        urllib.request.urlretrieve(self._image_url, image_file_path)

        self._article_image = image_file_path

    def _make_pdf(self) -> str:
        """
        Creates a pdf file containing the chosen article.
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
        if isinstance(self._article_text, str):
            pdf.set_font(tnr, size=12)
            pdf.set_y(pdf.get_y())
            pdf.multi_cell(150, 8, txt=self._article_text, align="L")

        article_title = re.sub(r"[^a-zA-Z0-9]", "", self._article_title)
        article_title = article_title.replace(" ", "")

        path = f"{self._tmpdir.name}/{article_title}.pdf"
        pdf.output(path)

        # returns the file name as a string
        self._pdf_name = f"{article_title}.pdf"

    def run(self):
        """
        Runs methods required for gathering article content.
        """
        self._get_html()
        self._parse_html()
        self._scrape_title()
        self._scrape_text()
        self._make_tmpdir()
        self._scrape_image()
        self._make_pdf()

    @property
    def tmpdir(self):
        return self._tmpdir

    @property
    def title(self):
        return self._article_title

    @property
    def text(self):
        return self._article_text

    @property
    def image(self):
        return self._article_image

    @property
    def pdf_name(self):
        return self._pdf_name
