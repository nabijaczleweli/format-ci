#!/usr/bin/python3


from github import Github
import subprocess
import datetime
import os

import data


gh = Github(os.getenv("GH_TOKEN"))


def handle_request(request_json, app):
	gh_repo = gh.get_repo(request_json["repository"]["full_name"])
	gh_commit = gh_repo.get_commit(request_json["after"])
	gh_commit.create_status("pending", context="continuous-integration/format-ci")

	this_job_id = data.max_job_id() + 1

	start_time = datetime.datetime.utcnow().timestamp()
	success = not build(request_json["repository"]["full_name"], request_json["after"], gh_repo, gh_commit, this_job_id, app)
	end_time = datetime.datetime.utcnow().timestamp()
	repo_id = data.update_repo_job_ids(request_json["repository"]["owner"]["name"], request_json["repository"]["name"], success, this_job_id)
	data.add_job(this_job_id, repo_id, success, start_time, end_time - start_time, request_json["after"])


def build(repo_slug, commit_id, gh_repo, gh_commit, job_id, app):
	clone_dir = "data/clones/{}/{}".format(repo_slug, commit_id)

	subprocess.run("git clone {} {}".format(gh_repo.clone_url, clone_dir), shell=True)
	subprocess.run("cd {} && git reset --hard".format(clone_dir), shell=True)

	if not os.path.exists(clone_dir + "/format-cieck"):
		gh_commit.create_status("error", description="Couldn't find format-cieck file", context="continuous-integration/format-ci")
		return 1

	log = ""
	failed_lines = 0
	with open(clone_dir + "/format-cieck") as fc:
		for line in fc:
			result = subprocess.run("cd {} && {}".format(clone_dir, line), shell=True, universal_newlines=True, stdout=subprocess.PIPE)
			log += "\n" + line + result.stdout
			if result.returncode is not 0:
				gh_commit.create_status("error", description="{} command failed with {} exit code".format(line, result.returncode),
				                                 context="continuous-integration/format-ci")
				++failed_lines
	with app.app_context():
		data.add_logs(job_id, log)
	print(log)

	if failed_lines is 0:
		gh_commit.create_status("success", description="Everything is formatted according to plan", context="continuous-integration/format-ci")

	return failed_lines
