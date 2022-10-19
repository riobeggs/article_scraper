from flask import Flask, render_template, request, send_from_directory

from assets.article_scraper import Article

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def home():
    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":
        url = request.form["url"]

        ar = Article(url)
        ar.run()
        return send_from_directory(ar.tmpdir.name, ar.pdf_name)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=8100, ssl_context="adhoc")