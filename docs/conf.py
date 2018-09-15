# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = 'PharmPy'
year = '2018'
authors = ['Rikard Nordgren', 'Gunnar Yngman']
copyright = '{0}; {1}'.format(year, ', '.join(authors))
version = release = '0.1.0'

pygments_style = 'trac'
templates_path = ['.']
# extlinks = {
#     'issue': ('https://github.com/rikardn/python-psn/issues/%s', '#'),
#     'pr': ('https://github.com/rikardn/python-psn/pull/%s', 'PR #'),
# }
import sphinx_py3doc_enhanced_theme
html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
# html_theme_options = {
#     'githuburl': 'https://github.com/rikardn/python-psn/'
# }

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
