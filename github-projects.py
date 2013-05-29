
'''
This grabs all your projects from github.

Configuration:

- gh username
? image-size

It then outputs:

[{
  "name": name,
  "id": id,
  "url":
  "description"
  "fork": bool
  "created_at"
  "updated_at"
  "pushed_at"
  "size"
  "watchers_count"
  "forks_count"
  "issues_count"
  "issues_url"
  "forks_url"
  "stargazers_url"
  "language"
  /// stuff I get additionally
  "readme": {file object}
  "logo": b64enc_png // looks first for logo.* in the base directory, then just for any image
  "contributors": [...]
},
...
]

- projects you are not a contributor on are filtered out
Sorted by:
- have you committed to this project? (if it's a fork)
- date last updated

'''

from functools import partial
from urllib2 import urlopen as upen
import logging
import json
import urllib2, base64
import getpass

pwd = None
def get_authd(username, url):
    global pwd
    if not pwd:
        pwd = getpass.getpass()

    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, pwd)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    return urllib2.urlopen(request)

def get_json(username, url):
    print 'getting', url
    try:
        return json.loads(get_authd(username, url).read())
    except:
        return False

GHAPI_PROJECTS = 'https://api.github.com/users/{username}/repos?per_page=1000'

def get_all_projects(username, max=None):
    data = get_json(username, GHAPI_PROJECTS.format(username=username))
    if not data:
        raise Error('failed to get data')
    if max:
        data = data[:int(max)]
    return map(partial(process_project, username), data)

def process_project(username, data):
    logging.debug('Processing {0}'.format(data['name']))
    keep_keys = ['id', 'name', 'full_name', 'html_url', 'description', 'fork',
        'created_at', 'updated_at', 'pushed_at', 'size', 'owner',
        'watchers_count', 'forks_count', 'issues_count', 'language',
        'stargazers_url', 'forks_url', 'issues_url', 'contributors_url',
        'contents_url']
    for k in data.keys():
        if k not in keep_keys:
            del data[k]
    if data['owner']['login'] != username:
        print 'Skipping {0}; not owner'.format(data['name'])
        return False
    # get contributors
    contributors = get_json(username, data['contributors_url'])
    if contributors:
        for person in contributors:
            if person['login'] == username:
                break
        else:
            return False # you haven't contributed to this project
    data['contributors'] = contributors
    # get readme and logo
    contents = get_json(username, data['contents_url'].format(**{'+path': ''}))
    data['readme'] = data['logo'] = None
    if not contents:
        return data
    fb_logos = ['logo.png', 'logo.gif', 'logo.jpg', 'logo.jpeg']
    pri_logos = ['logo-229x150.png', 'logo-229x150.gif',
                 'logo-229x150.jpg', 'logo-229x150.jpeg']
    for file in contents:
        if data['readme'] is None and file['name'].lower() in ['readme.rst', 'readme.md', 'readme']:
            pass #data['readme'] = get_json(username, file['url'])
        elif data['logo'] is None and\
                file['name'].lower() in fb_logos:
            data['logo'] = file
        elif file['name'].lower() in pri_logos and (data['logo'] is None
                                                    or data['logo']['name'].lower() in fb_logos):
            data['logo'] = file
    if not data['readme']:
        logging.debug('No readme found')
    if not data['logo']:
        logging.debug('No logo found')
    return data
    
def main():
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print 'Usage: github-projects.py username outfile.json [num]'
        sys.exit(1)
    data = get_all_projects(sys.argv[1], *sys.argv[3:])
    open(sys.argv[2], 'w').write(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
    
