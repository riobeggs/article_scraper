from fpdf import FPDF


def make_pdf(article_title: str, article_text: str):
    """
    Creates a pdf file containing the chosen article.

    Returns the file name as a string
    """

    article_text = article_text.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()
    pdf.set_top_margin(30)
    pdf.add_page()

    pdf.set_left_margin(30)

    # create title
    pdf.set_font("Times", size=26)
    pdf.multi_cell(150, 10, txt=article_title, align="L")

    # insert line break
    pdf.cell(150, 5, ln=2)

    # create text
    pdf.set_font("Times", size=12)
    pdf.multi_cell(150, 10, txt=article_text, align="L")

    article_title = article_title.replace(" ", "").replace("-", "")

    # save the pdf as article_title.pdf
    file = f"{article_title}.pdf"
    pdf.output(file)

    # returns the file name as a string
    return file
