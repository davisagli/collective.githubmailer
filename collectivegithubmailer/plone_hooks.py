"""Example script for updating hooks for all repositories in an organization."""

import sys
import json
import requests

requests.settings.verbose = sys.stderr

GH_URL = 'https://api.github.com'

# FILL THESE IN:
username = ''
password = ''

with requests.session(auth=(username, password)) as s:

    repos = list([r['name'] for r in json.loads(s.get(GH_URL+'/orgs/plone/repos').content)])
    for r in repos:

        hooks = json.loads(s.get(GH_URL+'/repos/plone/%s/hooks' % r).content)

        if not any(h['name'] == 'web' and h['config']['url'] == 'http://wglick.org/githubevent/' for h in hooks):
            req = {
                'name': 'web',
                'active': True,
                'config': {
                    'url': 'http://wglick.org/githubevent/',
                }
            }
            s.post(GH_URL+'/repos/plone/%s/hooks' % r, data=json.dumps(req))
        
        if not any(h['name'] == 'cia' for h in hooks):
            req = {
                'name': 'cia',
                'active': True,
                'config': {
                    'project': 'plone',
                    'branch': '%s',
                }
            }
            s.post(GH_URL+'/repos/plone/%s/hooks' % r, data=json.dumps(req))

        for h in hooks:
            if h['name'] == 'email' and h['config']['address'] == 'plone-cvs@lists.sourceforge.net':
                s.delete(GH_URL+'/repos/plone/%s/hooks/%s' % (r, h['id']))
