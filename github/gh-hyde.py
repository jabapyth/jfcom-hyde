#!/usr/bin/env python
'''
Takes a json file produced by github-projects, and creates all the project definition files
'''
import os
import json
import base64
import yaml
import re

TPL = open(os.path.join(os.path.dirname(__file__), 'project.html')).read()

RXS = {
    'tags': re.compile('{%\s*mark\s+tags\s*%}(.+?){%\s*endmark\s*%}', re.DOTALL),
    'long_description': re.compile('{%\s*mark\s+long_description\s*%}(.+?){%\s*endmark\s*%}',
                                   re.DOTALL)
}

def create_projects(fname, destdir):
    data = json.loads(open(fname).read())
    for project in data:
        if not project: continue
        print 'processing', project['name']
        context = {
            'tags': [str(project['language'])],
            'name': project['name'],
            'contents': 'No readme found',
            'created': project['created_at'],
            'updated': project['updated_at']
        }
        if project['readme']:
            text = base64.b64decode(project['readme']['content'])
            tags = RXS['tags'].findall(text)
            if tags:
                context['tags'] += str(tags[0]).split(',')
            long_desc = RXS['long_description'].findall(text)
            if long_desc:
                project['long_description'] = str(long_desc[0])
            else:
                project['long_description'] = project['description']
        # mk not doing contents atm
        if False and project['readme']:
            tag = None
            if project['readme']['name'].endswith('rst'):
                tag = 'restructuredtext'
            else:
                tag = 'markdown'
            contents = base64.b64decode(project['readme']['content'])
            context['contents'] = '{% ' + tag + ' %}{% raw %}\n'
            context['contents'] += contents.decode('utf8')
            context['contents'] += '\n{% endraw %}{% end' + tag + ' %}'

        if project['logo']:
            url = 'https://raw.github.com/{}/master/{}'.format(project['full_name'],
                                                               project['logo']['path'])
            project['logo_path'] = url
        else:
            project['logo_path'] = ''

        context['project'] = yaml.safe_dump({'project': project},
                                       default_flow_style=False)
        text = TPL % context
        open(os.path.join(destdir, project['name'] + '.html'), 'w').write(text.encode('utf8'))

def main():
    import sys
    if len(sys.argv) < 3:
        print 'Usage: gh-hyde.py projects.json dest/dir'
        sys.exit(1)
    create_projects(sys.argv[1], sys.argv[2])
        
if __name__ == '__main__':
    main()

