#!/usr/bin/env python

import sqlite3
import datetime
import os
import re

def get_posts(db_name):
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute('select * from blog_posts')
        posts = cur.fetchall()
        cols = [x[0] for x in cur.description]
        posts = [dict(zip(cols, post)) for post in posts]
    return posts

def fix_tilde(lines):
    for i in range(len(lines)):
        ln = lines[i].strip()
        if ln == '~' * len(ln):
            lines[i] = '^' * len(ln)

def get_ident(text):
    return re.match('^\s*', text).group()

def raw_code_blocks(lines):
    good = []
    ident = None
    in_block = False
    block = []
    for line in lines:
        if not in_block:
            if line.strip().startswith('.. code-block'):
                block.append(line)
                in_block = True
            else:
                good.append(line)
        else:
            if line.strip():
                if not ident:
                    ident = get_ident(line)
                elif get_ident(line) < ident:
                    in_block = False
                    ident = None
                    whole = '\n'.join(block)
                    if '{{' in whole or '{%' in whole:
                        block = ['{% raw %}'] + block + ['{% endraw %}']
                    good += block
                    good.append(line)
                    block = []
                    continue
            block.append(line)
    return good

def mark_body(text):
    text = text.replace('\r\n', '\n')
    text = text.strip().split('\n')
    fix_tilde(text)
    text = raw_code_blocks(text)
    image = []
    if text and text[0].startswith('.. image::'):
        while text and text[0].strip():
            image.append(text.pop(0))
    while text and not text[0].strip():
        text.pop(0)
    tease = []
    while text and text[0].strip():
        tease.append(text.pop(0))
    if image:
        image = ['{% mark image %}'] + image + ['{% endmark %}', '']
    if tease:
        tease = ['{% mark exerpt %}'] + tease + ['{% endmark %}', '']
    return '\n'.join(image + tease + text)

date_fmt = '%Y-%m-%d %H:%M:%S'
date_outfmt = '%Y/%b/%d/'

list_tpl = '''---
title: {}
extends: listing.j2
default_block: test
listable: false
---
'''

def output_listing(outdir, title):
    open(os.path.join(outdir, 'index.html'), 'w').write(list_tpl.format(title))

def output_listings(cdate, outdir):
    # make for year
    names = 'Posts for %Y', 'Posts for %B %Y', 'Posts for %B %d %Y'
    items = '%Y', '%b', '%d'
    for i in range(1, 4):
        d = cdate.strftime(os.path.join(outdir, *items[:i])).lower()
        if os.path.exists(d):
            continue
        os.makedirs(d)
        name = cdate.strftime(names[i-1])
        output_listing(d, name)

def output_post(data, outdir):
    tpl = '''---
title: {title}
slug: {slug}
created: !!timestamp '{created}'
extends: blog-rst.j2
status: {status}
{tags}
---
{body}
'''
    tags = '\n'.join('    - '+tag for tag in data['tags'].split(',') if tag.strip())
    if tags:
        tags = 'tags:\n' + tags
    text = tpl.format(title=repr(str(data['title'])),
            slug = data['slug'],
            created=data['publish'],
            status = ['', 'draft', 'public'][data['status']],
            tags=tags,
            body = mark_body(data['body'].encode('utf8')))
    date = datetime.datetime.strptime(data['publish'], date_fmt)
    output_listings(date, outdir)
    postdir = os.path.join(outdir, date.strftime(date_outfmt)).lower()
    if not os.path.exists(postdir):
        os.makedirs(postdir)
    fname = os.path.join(postdir, data['slug'] + '.html')
    print 'writing', fname
    open(fname, 'w').write(text)

def import_posts(db_name, outdir):
    posts = get_posts(db_name)
    for post in posts:
        output_post(post, outdir)

if __name__ == '__main__':
    import_posts('my.db', 'content/blog')


# vim: et sw=4 sts=4
