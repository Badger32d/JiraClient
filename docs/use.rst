Using JiraClient
****************


Use Cases
-----------
This Python JiraClient is intended to be a starting point for your scripts to interact with a jira server, either onsite or their hosted offering. You can use it to automatically create cases based on monitoring events, schedules, 
or to interface just about any python based script with your jira instance. 


Install
^^^^^^^^

Install via pip/easy_install will be offered in the near future. For now, you'll have to grab the source from github. 


Authentication
^^^^^^^^^^^^^^^

The JiraClient will need to know your authentication details to access Jira. For now it supports basic authentication (oauth to be added later), you can specify the details as environment variables or via a config file. See auth.cfg_example included in the source. 


