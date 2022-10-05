from assets.article_scraper import Article


def main():
    ar = Article()
    ar.scrape_text()
    ar.scrape_title()
    ar.create_txt_file()

if __name__ == "__main__":
    main()
