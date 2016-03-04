#!/usr/bin/python3


from flask import Flask, url_for, render_template
import os

import display
import data


app = Flask(__name__, template_folder="../assets/templates", static_folder="../assets/static")


@app.route("/")
def home():
	return render_template("home.html", display=display, data=data)


@app.teardown_appcontext
def close_db_connection(exception):
	data.close_db_connection(exception)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
