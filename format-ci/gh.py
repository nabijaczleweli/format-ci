#!/usr/bin/python3


from github import Github
from multiprocessing import Process
import subprocess
import sys
import os

import git


gh = Github(os.getenv("GH_TOKEN"))


def handle_request(request_json):
	gh_repo = gh.get_repo(request_json["repository"]["full_name"])
	clone_url = gh_repo.clone_url
	gh_commit = gh_repo.get_commit(request_json["after"])
	gh_commit.create_status("pending")

	builder = Process(target=build, args=(request_json["repository"]["full_name"], request_json["after"], gh_repo, gh_commit),
	                  name="Building {} #{}".format(request_json["repository"]["full_name"], request_json["after"]))
	builder.start()
	builder.join()

def build(repo_slug, commit_id, gh_repo, gh_commit):
	clone_dir = "data/clones/{}/{}".format(repo_slug, commit_id)

	subprocess.run("git clone {} {}".format(gh_repo.clone_url, clone_dir), shell=True)
	subprocess.run("cd {} && git reset --hard".format(clone_dir), shell=True)
