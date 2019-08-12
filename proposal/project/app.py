from flask import Flask
from flask import render_template
from app import app

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')