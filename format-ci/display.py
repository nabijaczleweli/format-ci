#!/usr/bin/python3


def cook_html(projects):
	toret = ""
	for project in projects:
		toret += project.__str__();
	return toret
