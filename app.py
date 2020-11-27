from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, Text
import server

domain = "0.0.0.0:5000/"
number = 0
templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"] )
def tiny():
    url = request.args.get("url", "")
    optional = request.args.get("optional", "")
    find = request.args.get("find", "")
    if (optional == "" and url):
        #url se va al redis y se crea el random URL
        token = server.generateRandomKey()
        server.setNewLink(token, url)
        return render_template("myURL.html", link = token, domain = domain)
    elif (optional):
        #si optional si trae algun input se crea URL con ese input
        server.setNewLink(optional, url)
        return render_template("myURL.html", link = optional, domain = domain)
    elif (find):
        return redirect(url_for('search', token = find))
    return render_template("tiny.html")

@app.route("/<link>", methods = ["GET"])
def redirectURL (link):
    if link in server.getAllLinks():
        ogURL = server.getLink(link)
        server.setNewVisit(link)
        return redirect(ogURL)
    return page_not_found(401)
    

@app.route("/urls", methods=["GET", "POST"])
def urls():
    url = "url"
    time = 'time'
    find = request.args.get("find", "")
    if request.method == "POST":
        token = request.form["remove"]
        server.deleteURL(token)
        allLinks = server.getAllLinks()
        return render_template("urls.html", links = allLinks, domain = domain, url = url, time = time)
    elif (find):
        return redirect(url_for('search', token = find))
    allLinks = server.getAllLinks()
    return render_template("urls.html", links = allLinks, domain = domain, url=url, time = time)

@app.route("/stats", methods = ["GET", "POST"])
def stats():
    url = "url"
    visits = "visits"
    time = 'time'
    find = request.args.get("find", "")
    if (find):
        return redirect(url_for('search', token = find))
    return render_template("stats.html", links = server.getAllLinks(), url = url, visits = visits, time = time, domain = domain)


@app.route("/about", methods = ["GET", "POST"])
def about():
    find = request.args.get("find", "")
    if (find):
        return redirect(url_for('search', token = find))
    return render_template("about.html")

@app.route("/search/<token>")
def search(token):
    url = 'url'
    time = 'time'
    info = server.getInfo(token)
    return render_template("search.html", name = token, info = info, url = url, time = time)

@app.route("/thanks")
def thankYou():
    return render_template("thankyou.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_found.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
