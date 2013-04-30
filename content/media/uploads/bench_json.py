#!/usr/bin/env python

import ppjson
from codetalker.contrib import json
import jsonply

text = open('../json_testbed/large_doc.json').read()

import timeit

# text = '{"f":null, "amb":"cfd", "hoo":["eo",3]}'

pp = ppjson.loads(text)
ct = json.loads(text)
pl = jsonply.loads(text)
print pp==ct
print ct==pl
print pp==pl

num=100
a = timeit.timeit('ppjson.loads(text)', 'from __main__ import text,ppjson', number=num)/num
b = timeit.timeit('json.loads(text)', 'from __main__ import text,json', number=num)/num
c = timeit.timeit('jsonply.loads(text)', 'from __main__ import text,jsonply', number=num)/num
print 'pp',a
print 'ct',b
print 'ply',c
open('out.log','w').write(str([a,b,c]))


# vim: et sw=4 sts=4
