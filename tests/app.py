import logging
import os
import unittest
from unittest.mock import MagicMock, Mock

from assets.article_scraper import Article
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
