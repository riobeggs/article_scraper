from assets.article_scraper import Article
from assets.pdf_maker import make_pdf
from assets.open_article import read_article


def main():
    ar = Article()
    ar.scrape_title()
    ar.scrape_text()
    ar.scrape_image()
    article_pdf = make_pdf(ar.article_title, ar.article_text, ar.article_image)
    read_article(article_pdf)

if __name__ == "__main__":
    main()
