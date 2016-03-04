#!/usr/bin/python3


from flask import g
import sqlite3


DATABASE = "format-ci.db"


class Project:
	def __init__(self, ):
		self.arg = arg


def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
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
		              	username TEXT,
		              	repo_name TEXT,
		              	passed BOOLEAN,
		              	job_amount UNSIGNED INTEGER,
		              	CHECK (job_amount > 0)
		          );''')
		db.commit()
		c.close()


def projects():
	get_db()
	return []
