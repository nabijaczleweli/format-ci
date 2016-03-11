#!/usr/bin/python3


from flask import render_template

import data


def cook_projects_html(projects):
	return "".join(map(lambda pr: render_template("repo_box.html", repo_owner=pr[0], repo_name=pr[1], repo_passed=pr[2], repo_job_amount=pr[3],
	                                              last_job_id=eval(pr[4])[-1]), projects))

def cook_job_log(job):
	if job is not None:
		return "<pre>" + job[0].replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
	else:
		return ""

def cook_repo(repo):
	return "".join(map(lambda id: _cook_job_in_repo(data.job(id), repo[0], repo[1]), reversed(eval(repo[2]))))


def _cook_job_in_repo(job, repo_owner, repo_name):
	return render_template("job_box.html", job_id=job[0], job_passed=job[1], job_commit_hash=job[5], repo_owner=repo_owner, repo_name=repo_name)
