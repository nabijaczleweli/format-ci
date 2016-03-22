#!/usr/bin/python3


from smtplib import SMTP
import os


def notify(email_addresses, job_id, repo_job_num, repo_name, commit):
	own_addr, server = _connect_to_mail_server()

	if own_addr is None or server is None:
		return

	server.sendmail(own_addr, email_addresses, "\r\n".join([
		"From: {}".format(own_addr),
		"To: {}".format(", ".join(email_addresses)),
		"Subject: {} #{} failed".format(repo_name, repo_job_num),
		"",
		"Job #{} of {} triggered by commit {} failed.".format(repo_job_num, repo_name, commit),
		"Visit {}/job/{} for details.".format(os.getenv("OWN_URL"), job_id),
	]))
	server.quit()


def _connect_to_mail_server():
	if os.getenv("GMAIL_USERNAME") is None or os.getenv("GMAIL_PASSWORD") is None:
		return (None, None)

	own_addr = os.getenv("GMAIL_USERNAME") + "@gmail.com"
	gmail = SMTP("smtp.gmail.com:587")

	gmail.ehlo()
	gmail.starttls()
	gmail.login(own_addr, os.getenv("GMAIL_PASSWORD"))

	return (own_addr, gmail)
