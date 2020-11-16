from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import random, string

templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

domain = "https://domain.com/"

def generateRandomKey ():
    key = string.ascii_lowercase + string.digits
    randomKey = ''.join((random.choice(key) for i in range(8)))
    result = domain + randomKey
    return result

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"] )
def tiny():
    url = request.args.get("url", "")
    optional = request.args.get("optional", "")
    if (optional != ""):
        #url se va al redis y se crea el random URL
        pass
    #si optional si trae algun input se crea URL con ese input

    return render_template("tiny.html")

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Thanks")
def thankYou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
