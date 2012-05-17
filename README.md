JiraClient
==========

STATUS: Alpha


JiraClient is a python client for Jira's REST API (version 2).
This is a work in progress to replace a client I wrote for their older APIs.


USE:
If you want to try the code as-is, take a look at scratchpad.py for a few examples.

Authentication:
Currently only supports basic authentication, you can set the auth details via environment variables or create a config file.

Envionment Variables - set three environment variables (JIRA_API_USER, JIRA_API_PASS, JIRA_API_URL)
Config File - see auth.cfg_example and configure with your details, then save as auth.cfg