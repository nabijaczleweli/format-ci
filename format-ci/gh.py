#!/usr/bin/python3


from github import Github
import os


gh = Github(client_id=os.getenv("GH_CLIENT_ID"), client_secret=os.getenv("GH_CLIENT_SECRET"), user_agent="format-ci/Python")


def handle_request(request_json):
	pass
