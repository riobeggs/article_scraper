import urllib.request
import re


def download_image(title, url) -> str:
    if isinstance(url, str):
        title = re.sub(r"[^a-zA-Z0-9]", "", title)
        image_file_path = f"/Users/riobeggs/Documents/code/nzherald_webscraper/assets/images/{title}.jpg"
        urllib.request.urlretrieve(url, image_file_path)

        return image_file_path
