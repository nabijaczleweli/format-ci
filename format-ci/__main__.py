#!/usr/bin/python3


from flask import Flask, render_template, request
import os
import sys

import display
import data
import gh


app = Flask(__name__, template_folder="../assets/templates", static_folder="../assets/static")


@app.route("/")
def home():
	return render_template("home.html", display=display, data=data)

@app.route("/<username>")
def user(username):
	return render_template("user.html", display=display, data=data, username=username)

@app.route("/<username>/<reponame>")
def repo(username, reponame):
	return render_template("repo.html", display=display, data=data, username=username, reponame=reponame)

@app.route("/job/<int:id>")
def show_job(id):
	project = data.project_from_job_id(id)
	job = data.job(id)
	return render_template("job.html", display=display, data=data, job_id=id, project_owner=project[1], project_name=project[2],
	                       new_commit=job[5], old_commit=job[6], job_passed=job[1])

@app.route("/github_callback", methods=["POST"])
def receive_github_request():
	gh.handle_request(request.get_json(), app)
	return ""


@app.teardown_appcontext
def close_db_connection(exception):
	data.close_db_connection(exception)


if __name__ == "__main__":
	if os.getenv("GH_TOKEN") is None:
		sys.stderr.write("Environment variable GH_TOKEN not set. Set it to the OAuth token format-ci should be using.\n")
		sys.exit(1)

	if os.getenv("OWN_URL") is None:
		sys.stderr.write("Environment variable OWN_URL not set. Set it to the external URL of this site.\n")
		sys.exit(1)

	if os.getenv("PAYLOAD_URL") is None:
		sys.stderr.write("Environment variable PAYLOAD_URL not set. Set it to the URL users are instructed to point their webhooks to. "
		                 "Default: $OWN_URL/github_callback.\n")

	if os.getenv("GMAIL_USERNAME") is None:
		sys.stderr.write("Environment variable GMAIL_USERNAME not set. Set it to username on GMail. Disabling mail.\n")
	if os.getenv("GMAIL_PASSWORD") is None:
		sys.stderr.write("Environment variable GMAIL_PASSWORD not set. Set it to password on GMail. Disabling mail.\n")

	app.run(host="0.0.0.0", port=int(os.getenv("PORT", "1082")))
