#!/usr/bin/env python

import jinja2
from jinja2 import evalcontextfilter

import re

rx = re.compile('^---\n(.*\n)*?---\n')

@evalcontextfilter
def strip_meta(ctx, html):
    if not html:
        return ''
    res = rx.sub('', unicode(html))
    return res

def Dummy(*a, **b):
    pass

# vim: et sw=4 sts=4
