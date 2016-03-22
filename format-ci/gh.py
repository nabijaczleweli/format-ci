#!/usr/bin/python3


from github import Github
import subprocess
import datetime
import os

import data
import mail


gh = Github(os.getenv("GH_TOKEN"))


def handle_request(request_json, app):
	if "commits" not in request_json:  # Top-level "commits" only in https://developer.github.com/v3/activity/events/types/#pushevent
		return

	gh_repo = gh.get_repo(request_json["repository"]["full_name"])
	gh_commit = gh_repo.get_commit(request_json["after"])
	gh_commit.create_status("pending", context="continuous-integration/format-ci")

	this_job_id = data.max_job_id() + 1

	start_time = datetime.datetime.utcnow().timestamp()
	success = not build(request_json["repository"]["full_name"], request_json["after"], gh_repo, gh_commit, this_job_id, app)
	end_time = datetime.datetime.utcnow().timestamp()
	repo_id, repo_job_num = data.update_repo_job_ids(request_json["repository"]["owner"]["name"], request_json["repository"]["name"], success, this_job_id)
	data.add_job(this_job_id, repo_id, success, start_time, end_time - start_time, request_json["after"], request_json["before"])

	if not success:
		mail.notify(set([request_json["head_commit"]["author"]["email"], request_json["head_commit"]["committer"]["email"],
		                 request_json["repository"]["owner"]["email"]]),
		            this_job_id, repo_job_num, request_json["repository"]["full_name"], request_json["after"])


def build(repo_slug, commit_id, gh_repo, gh_commit, job_id, app):
	clone_dir = "data/clones/{}/{}".format(repo_slug, commit_id)

	log = ""
	for command in [
		"git clone {} {}".format(gh_repo.clone_url, clone_dir),
		"cd {} && git reset --hard {}".format(clone_dir, commit_id)
	]:
		log += command + "\n" + subprocess.run(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout + "\n"

	if not os.path.exists(clone_dir + "/.format-cieck"):
		gh_commit.create_status("error", description="Couldn't find .format-cieck file", context="continuous-integration/format-ci")
		return 1

	format_result = subprocess.run("bash", input="""cd {}
set -e
set -v
{}""".format(clone_dir, _read_whole_file(clone_dir + "/.format-cieck")), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	log += format_result.stdout + "\n" + format_result.stderr
	with app.app_context():
		data.add_logs(job_id, log)

	if format_result.returncode is 0:
		gh_commit.create_status("success", description="Everything is formatted according to plan", context="continuous-integration/format-ci")
	else:
		gh_commit.create_status("error", description="Format checking failed with {} exit code".format(format_result.returncode),
		                        context="continuous-integration/format-ci")

	return format_result.returncode

def _read_whole_file(path):
	with open(path) as f:
		return f.read()
