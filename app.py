from assets.article_scraper import Article
from assets.pdf_maker import make_pdf
from assets.open_article import read_article


def main():
    ar = Article()
    ar.scrape_text()
    ar.scrape_title()
    article_pdf = make_pdf(ar.article_name, ar.article_text)
    read_article(article_pdf)

if __name__ == "__main__":
    main()
