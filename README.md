# Article Scraper

This Article Scraper was designed so that the user can read any article solely as a PDF without the distraction of ads and irrelevant information. I chose to base the project on scraping a local news publishing website, NZ Herald (https://www.nzherald.co.nz).

## Installation

Create a Virtual environment named .venv
```bash
python3 -m venv .venv
```

Activate the virtual environment. 
```bash
source .venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.
```bash
source .venv/bin/activate
pip install requirements.txt
```

## Usage
Run the Article Scraper
```bash
python3 app.py
```
1. Open a browser and visit the Article Scraper Flask web server at https://127.0.0.1:8100
2. Visit NZ Herald at https://www.nzherald.co.nz
3. Select any article whether it is free or premium, and copy the URL.
4. Paste the URL into the Article Scraper web server.
5. A PDF of your article should automatically open in the browser.
