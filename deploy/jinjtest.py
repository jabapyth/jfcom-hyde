import jinja2
import jinja2.ext
import pyjade

class JadeExtension(jinja2.ext.Extension):
    tags = set(['jade'])

    def __init__(self, environment):
        super(JadeExtension, self).__init__(environment)
        environment.extend(
            pyjade=pyjade.process
        )   

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endjade'],
            drop_needle=True
        )
        return jinja2.nodes.CallBlock(
            self.call_method('_jade_support'),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _jade_support(self, caller):
        return self.environment.pyjade(caller()).strip()

env = jinja2.Environment(extensions=[JadeExtension])

text = """ 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <body>    <mensch></mensch>  </body>
</html>
"""

html = env.from_string(text).render(two='Two')

print html