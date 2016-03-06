#!/usr/bin/python3


from flask import g
import os
import sqlite3


DATABASE = "data/format-ci.db"


def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		try:
			db = g._database = sqlite3.connect(DATABASE)
		except sqlite3.OperationalError:
			os.mkdir(os.path.dirname(DATABASE))
			return get_db()
		_init_db(db)
	return db

def close_db_connection(exception):
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()

def _init_db(db):
	c = db.cursor()
	c.execute('''SELECT * FROM sqlite_master WHERE name="repositories" and type="table";''')
	if c.fetchone() is None:
		c.execute('''CREATE TABLE repositories(
		            	ID INTEGER PRIMARY KEY,
		             	username TEXT,
		             	repo_name TEXT,
		             	passed BOOLEAN,
		             	job_amount UNSIGNED INTEGER,
		             	job_ids TEXT,
		             	CHECK (job_amount > 0)
		          );''')
	c.execute('''SELECT * FROM sqlite_master WHERE name="jobs" and type="table";''')
	if c.fetchone() is None:
		c.execute('''CREATE TABLE jobs(
		            	ID INTEGER PRIMARY KEY,
		             	passed BOOLEAN,
		             	repo_id INTEGER,
		             	start_time TEXT,
		             	duration UNSIGNED INTEGER,
		             	commit_id TEXT,
		             	CHECK (duration > 0)
		          );''')
	db.commit()
	c.close()


def projects():
	c = get_db().cursor()
	toret = list(c.execute('''SELECT repositories.username,repositories.repo_name,repositories.passed,repositories.job_amount,repositories.job_ids
	                          	FROM repositories;'''))
	c.close()
	return toret

def project_from_job_id(job_id):
	import sys
	c = get_db().cursor()
	c.execute('''SELECT jobs.repo_id FROM jobs WHERE jobs.ID is ?;''', (job_id,))
	c.execute('''SELECT * FROM repositories WHERE repositories.ID is ?;''', c.fetchone())
	repo = c.fetchone()
	c.close()
	return repo
