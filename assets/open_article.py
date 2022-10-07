import subprocess

def read_article(article_pdf) -> None:
    subprocess.call(['open', '-a', 'Preview', article_pdf])