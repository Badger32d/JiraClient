#!/usr/bin/env python
'''
WeatherAlerts.nws
*******************

File Information
==================

**Project Home:**
  http://github.com/zebpalmer/JiraClient

**Original Author:**
  Zeb Palmer http://www.zebpalmer.com

**License:**
  GPLv3 - full text included in LICENSE.txt


License Notice:
"""""""""""""""""
This program is free software you can redistribute it and or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.  You should have received a copy of the GNU General Public
License along with this program. If not, see <http://www.gnu.org/licenses/>.

----------------------------------------------------------------------------------------------------------------

'''



import os
import time
import requests
import json


class AuthenticationFailure(Exception):
    '''Custom Exception class for Authentication failures'''
    pass

class ConnectionFailure(Exception):
    '''Custom Exception class for Connection failures'''
    pass

class JQLError(Exception):
    '''Custom Exception class for failed JQL queiries'''
    pass

class Auth():
    '''Currently only supports authentication details from environment variables
    need to add ability to set auth on the fly and add oauth support as well'''
    def __init__(self, auth_type, authfile=None):
        if auth_type == 'basic_env':
            try:
                self.user = os.environ['JIRA_API_USER']
                self.pwd = os.environ['JIRA_API_PASS']
                self.url = os.environ['JIRA_API_URL']
            except KeyError:
                print "Auth Environment Variables Not Set"
            except Exception, e:
                print e
                raise
        elif auth_type == 'basic_file':
            import ConfigParser
            config = ConfigParser.RawConfigParser()
            config.read(authfile)
            self.user = config.get('JIRA Auth', 'username')
            self.pwd = config.get('JIRA Auth', 'password')
            self.url = config.get('JIRA Auth', 'url')

class Case(object):
    '''Case object'''
    #FIXME this is a bit rough, needs to be ironed out a bit
    def __init__(self, case_json):
        '''iterate through the incoming '''
        for key in case_json:
            if isinstance(case_json[key], dict):
                self.__dict__[key] = Case(case_json[key])
            elif isinstance(case_json[key], (list, tuple)):
                tmplist = []
                for value in case_json[key]:
                    if isinstance(value, dict):
                        tmplist.append(Case(value))
                    elif isinstance(value, (list)):
                        tmplist2 = []
                        for item in value:
                            if isinstance(item, dict):
                                tmplist2.append(Case(item))
                        tmplist.append(tmplist2)
                        del(tmplist2)
                    else:
                        tmplist.append(value)
                self.__dict__[key] = tmplist
            else:
                self.__dict__[key] = case_json[key]


    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __repr__(self):
        import pprint
        return pprint.pformat(self.__dict__)


class Jira(object):
    def __init__(self, auth):
        self.auth = auth
        self.baseurl = '''{0}rest/api/2/'''.format(self.auth.url)

    def _jira_get(self, target_url, max_attempts=3):
        '''retrieves a url, attempts to parse the result to json'''
        attempt = 0
        while attempt < max_attempts:
            response = requests.get(target_url, auth=(self.auth.user, self.auth.pwd))
            if response.status_code == 200:
                try:
                    return json.loads(str(response.content))
                except Exception:
                    return response.content
            elif response.status_code == 401:
                raise AuthenticationFailure
            else:
                time.sleep(1)
        raise ConnectionFailure


    def _jira_post(self, target_url, content):
        '''Does a HTTP Post to the target url with the  '''
        headers = {'content-type': 'application/json'}
        payload = json.dumps(content)
        response = requests.post(target_url, auth=(self.auth.user, self.auth.pwd), data=payload, headers=headers)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 400:
            #fixme
            print json.loads(response.content)['errorMessages'][0]
            raise JQLError
        else:
            print response.status_code
            print response.content


    def get(self, ids):
        cases = []
        for key in ids:
            req_url = '''{0}{1}/{2}'''.format(self.baseurl, 'issue', key)
            results = self._jira_get(req_url)
            cases.append(Case(json.loads(str(results).strip())))
        return cases


    def search(self, jql, startat=0, maxresults=100, fields=''):
        cases = []
        req_url = self.baseurl + 'search'
        req_content = { "jql": jql,
                        "startAt": startat,
                        "maxResults": maxresults
                        }
        if fields != '':
            req_content['fields'] = fields
        result = self._jira_post(req_url, req_content)
        content = json.loads(result)
        if content["total"] > maxresults:
            return "Error: Results larger than max result"
        else:
            for case in content['issues']:
                cases.append(Case(case))

        return cases

    def create_case(self):
        #fixme: need to implement
        pass




    def add_comment(self, case_id, comment):
        req_url = self.baseurl + str(case_id) + "/comment"
        req_content = {"body": comment}
        self._jira_post(req_url, req_content)


    @property
    def createmeta(self):
        req_url = '''{0}issue/createmeta'''.format(self.baseurl)
        return self._jira_get(req_url)


    @property
    def serverinfo(self):
        req_url = self.baseurl + 'serverInfo'
        result = self._jira_get(req_url)
        return result

    def test_connection(self):
        status = self.serverinfo
        msg = '''{0} -- {1} -- version {2}'''.format(status['serverTitle'], status['baseUrl'], status['version'])
        return msg

if __name__ == "__main__":
    jira = Jira(Auth('basic'))
