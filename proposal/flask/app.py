from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/industry")
def industry_page():
    return render_template("industry.html")

@app.route("/score")
def score_page():
    return render_template("score.html")

if __name__ == "__main__":
    app.run(debug=True)
