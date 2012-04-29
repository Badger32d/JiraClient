#!/usr/bin/evn python

import jiraclient






if __name__ == "__main__":
    #create jira object passing auth instance
    jira = jira.Jira(jira.Auth('basic'))

    #ids = ['SYS-2']
    #cases = jira.get(ids)
    #for case in cases:
        #print case.fields.reporter.name
        #print case.fields.comment.comments[0].body
        #print case.fields.created
        #print case.id

    # print jira.createmeta


    # result = jira.search("project = System")
    # for case in result:
        #print case.key

    # print jira.serverinfo

    # jira.add_comment('SYS-43', "test comment from the REST API client")



