from __future__ import unicode_literals

import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.githubpages',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'jupyter_sphinx',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = 'Pharmpy'
year = '2018-2020'
authors = ['the Pharmpy development team']
copyright = '{0}; {1}'.format(year, ', '.join(authors))
version = release = '0.3.0'

pygments_style = 'trac'
templates_path = ['.']

html_theme = "pydata_sphinx_theme"

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

# if this is True, todo and todolist produce output, else they produce nothing
todo_include_todos = True

# inheritance_graph_attrs = dict()
# inheritance_node_attrs = dict(font='Palatino', color='gray50', fontcolor='black')
# inheritance_edge_attrs = dict(color='maroon')
# graphviz_output_format = 'svg'
