from flask import Flask, render_template, request
from pipeline import chain, config


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    text = ""
    pdf_name = ""

    if request.method == "POST":

        text = request.form.get("message", "")

        pdf = request.files.get("pdf")

        if pdf and pdf.filename:
            pdf_name = pdf.filename

    print(text, pdf_name)
    return render_template(
        "index.html",
        text=text,
        pdf_name=pdf_name
    )


if __name__ == "__main__":
    app.run(debug=True)