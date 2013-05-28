import jinja2
import jinja2.ext
import pyjade
import pyjade.ext.jinja
import re
from jinja2.runtime import Undefined

from pyjade.runtime import attrs as _attrs, iteration
import metastrip

ATTRS_FUNC = '__pyjade_attrs'
ITER_FUNC = '__pyjade_iter'

def attrs(attrs, terse=False):
    return _attrs(attrs, terse)

class JadeExtension(jinja2.ext.Extension):
    tags = set(['jade'])
    tags_rx = re.compile('{%\s*jade\s*%}'), re.compile('{%\s*endjade\s*%}')

    def __init__(self, env):
        env.filters['strip_meta'] = metastrip.strip_meta
        env.globals[ATTRS_FUNC] = attrs
        env.globals[ITER_FUNC] = iteration
        env.globals['str'] = str
        return super(JadeExtension, self).__init__(env)

    def preprocess(self, source, name, filename = None):
        if (name and name.endswith('.jade')) or (filename and filename.endswith('.jade')):
            return pyjade.process(source, compiler=pyjade.ext.jinja.Compiler)
        result = ''
        start_pos = 0
        while start_pos < len(source) - 1:
            match = self.tags_rx[0].search(source, start_pos)
            if not match:
                return result + source[start_pos:]
            result += source[:match.start()]
            start_pos = match.end()
            close = self.tags_rx[1].search(source, start_pos)
            if not close:
                raise TemplateSyntaxError('Expecting "endjade" tag', result.count('\n'))
            raw = source[match.end():close.start()]
            result += pyjade.process(raw, compiler=pyjade.ext.jinja.Compiler)
            start_pos = close.end()
        return result

def test():
    env = jinja2.Environment(extensions=[JadeExtension])

    text = """ 
    {% jade %}
    !!!
    html
        body
            block content
                mensch
    {% endjade %}
    """

    html = env.from_string(text).render(two='Two')

    print html
