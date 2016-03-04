#!/usr/bin/python3


from flask import Flask, url_for, render_template
import sqlite3
import os


app = Flask(__name__, template_folder="../assets")


@app.route("/")
def hello():
	return "Hello World!"

@app.route("/blerb")
def blerb():
	return render_template("home.html")


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=os.getenv("PORT", "5000"))
