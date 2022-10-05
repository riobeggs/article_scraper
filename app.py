from assets.article_scraper import Article


def main():
    ar = Article()
    ar.scrape_text()
    print(ar.article_text)


if __name__ == "__main__":
    main()
