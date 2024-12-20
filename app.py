from flask import Flask, render_template, request, redirect, url_for
from main import process_keyword_year

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    # Get input data from the form
    keyword = request.form.get("keyword")
    year = request.form.get("year")

    if not keyword or not year:
        return "Please provide both a keyword and a year."

    try:
        # Call the correct function
        process_keyword_year(keyword, int(year))
        return redirect(url_for("results"))
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)
