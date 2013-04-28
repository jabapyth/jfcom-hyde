#!/usr/bin/env python

import sqlite3
import datetime

def get_posts(db_name):
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        if not os.path.exists(outdir):
            os.path.makedirs(outdir)
        cur.execute('select * from blog_posts')
        posts = cur.fetchall()
        cols = [x[0] for x in cur.description]
        posts = [dict(zip(cols, post)) for post in posts]
    return posts

def mark_body(text):
    text=text.strip().split('\n')
    image = []
    if text[0].startswith('.. image::'):
        for line in text:
            if not line.strip():
                break
            image.append(line)
        text = text[len(image):]
    while not text[0].strip():
        text.pop(0)
    tease = []
    while text[0].strip():
        tease.append(text[0])
    if image:
        image = ['{% mark image -%}'] + image + ['{%- endmark %}', '']
    if tease:
        tease = ['{% mark exerpt -%}'] + tease + ['{%- endmark %}', '']
    return '\n'.join(image + tease + text)

date_fmt = '%Y-%m-%d %H:%M:%S'
date_outfmt = '%Y/%b/%d/'

def output_post(data, outdir):
    tpl = '''---
title: {title}
created: !!timestamp '{created}'
extends: blog-rst.j2
tags:
{tags}
---
{body}
'''
    text = tpl.format(title=data['title'],
            created=data['publish'],
            tags='\n'.join('    - '+tag for tag in data['tags'].split(',')),
            body = mark_body(data['body'])
    date = datetime.datetime.strptime(data['publish'], date_fmt)
    postdir = os.path.join(outdir, date.strftime(date_outfmt))
    if not os.path.exists(postdir):
        os.path.makedirs(postdir)
    fname = os.path.join(postdir, data['slug'] + '.html')
    open(fname, 'w').write(text)

def import_posts(db_name, outdir):
    posts = get_posts(db_name)
    for post in posts:
        output_post(post, outdir)

if __name__ == '__main__':
    import_posts('my.db', 'content/blog')


# vim: et sw=4 sts=4
