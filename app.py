from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import random, string
import server

domain = "https://makeItTiny.com/"

templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"] )
def tiny():
    url = request.args.get("url", "")
    optional = request.args.get("optional", "")
    if (optional == "" and url):
        #url se va al redis y se crea el random URL
        token = server.generateRandomKey(domain)
        server.setNewLink(token, url)
        return render_template("myURL.html", link = token)
    elif (optional):
        #si optional si trae algun input se crea URL con ese input
        token = server.generateOptionalKey(optional, domain)
        server.setNewLink(token, url)
        return render_template("myURL.html", link = token)
    return render_template("tiny.html")

@app.route("/urls", methods=["GET", "POST"])
def urls():
    token = request.args.get("getKey()", "")
    print(token)
    if (token):
        server.deleteURL(token)
        return render_template("urls.html", links = server.getAllLinks())
    return render_template("urls.html", links = server.getAllLinks())

@app.route("/delete")
def delete():
    token = request.args.get("name")
    #dic = server.getAllLinks()
    #list_links = list(dic)
    #token = list_links[position]
    server.deleteURL(token)
    return render_template("urls.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/thanks")
def thankYou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
