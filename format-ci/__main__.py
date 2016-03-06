#!/usr/bin/python3


from flask import Flask, render_template, request
import os
import sys
import json

import display
import data
import gh


app = Flask(__name__, template_folder="../assets/templates", static_folder="../assets/static")


@app.route("/")
def home():
	return render_template("home.html", display=display, data=data)

@app.route("/job/<int:id>")
def show_job(id):
	project = data.project_from_job_id(id)
	return render_template("job.html", display=display, data=data, job_id=id, project_owner=project[1], project_name=project[2])

@app.route("/github_callback", methods=["POST"])
def receive_github_request():
	gh.handle_request(request.get_json())
	return ""


@app.teardown_appcontext
def close_db_connection(exception):
	data.close_db_connection(exception)


if __name__ == "__main__":
	if os.getenv("GH_CLIENT_ID") is None:
		sys.stderr.write("Environment variable GH_CLIENT_ID not set. Set it to the developer application ID.\n")
		sys.exit(1)
	if os.getenv("GH_CLIENT_SECRET") is None:
		sys.stderr.write("Environment variable GH_CLIENT_SECRET not set. Set it to the developer application's secret.\n")
		sys.exit(1)
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
