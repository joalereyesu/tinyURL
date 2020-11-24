from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import random, string
import server

domain = "0.0.0.0:5000/"

templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"] )
def tiny():
    url = request.args.get("url", "")
    optional = request.args.get("optional", "")
    if (optional == "" and url):
        #url se va al redis y se crea el random URL
        token = server.generateRandomKey()
        server.setNewLink(token, url)
        return render_template("myURL.html", link = token, domain = domain)
    elif (optional):
        #si optional si trae algun input se crea URL con ese input
        server.setNewLink(optional, url)
        return render_template("myURL.html", link = optional, domain = domain)
    return render_template("tiny.html")

@app.route("/<link>", methods = ["GET"])
def redirectURL (link):
    if link in server.getAllLinks():
        ogURL = server.getLink(link)
        server.setNewVisit(link)
        return redirect(ogURL)
    else:
        """notfound"""

@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        token = request.form["remove"]
        server.deleteURL(token)
        return render_template("urls.html", links = server.getAllLinks(), domain = domain)
    return render_template("urls.html", links = server.getAllLinks(), domain = domain)

@app.route("/stats")
def stats():
    return render_template("stats.html", links = server.getAllLinks(), visits = server.getAllLinksVisits(), domain = domain)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/thanks")
def thankYou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
