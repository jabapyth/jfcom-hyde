#!/usr/bin/env python

import pytest
import djangohyde

@pytest.mark.parametrize(('inp', 'outp'), (
    ('', ''),
    ('~~~', '^^^'),
    ('~~~\nhi', '^^^\nhi')
))
def test_fix_tilde(inp, outp):
    print inp, outp
    lines = inp.split('\n')
    djangohyde.fix_tilde(lines)
    assert '\n'.join(lines) == outp

@pytest.mark.parametrize(('text', 'ind'), (
    ('', 0),
    ('hi', 0),
    (' hi', 1),
    ('a b', 0),
    ('  g    ', 2),
    ('        ', 8)
))
def test_get_indent(text, ind):
    assert djangohyde.get_ident(text) == ind

@pytest.mark.parametrize(('inp', 'outp'), (
('''hello

.. code-block:: python
    
    {% man %}

done''',
'''hello

{% raw %}
.. code-block:: python
    
    {% man %}

{% endraw %}
done'''),
('''hello

.. code-block:: python
    
    {{man}}

done''',
'''hello

{% raw %}
.. code-block:: python
    
    {{man}}

{% endraw %}
done'''),
('''hello

.. code-block:: python
    
    def manhatten():
        print {{hello}}

        if name==name:
            print goodbye
    
    more

done''',
'''hello

{% raw %}
.. code-block:: python
    
    def manhatten():
        print {{hello}}

        if name==name:
            print goodbye
    
    more

{% endraw %}
done'''),
('''hello

.. code-block:: python
    
    def manhatten():
        print hello

        if name==name:
            print goodbye
    
    more

done''',
True),
))
def test_raw_code_blocks(inp, outp):
    lines = inp.split('\n')
    res = djangohyde.raw_code_blocks(lines)
    if outp is True:
        outp = inp
    
    assert '\n'.join(res) == outp

@pytest.mark.parametrize(('inp', 'outp'), (
('''
''',''''''),
('''
hello
''', '''{% mark excerpt %}
hello
{% endmark %}
'''),
('''
.. image:: manhatten.png
''','''{% mark image %}
.. image:: manhatten.png
{% endmark %}
''')
))
def test_mark_body(inp, outp):
    assert djangohyde.mark_body(inp) == outp

# vim: et sw=4 sts=4
