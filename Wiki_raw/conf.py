# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../Alpaga'))


# -- Project information -----------------------------------------------------

project = 'Alpaga'
copyright = 'L-GPL'
author = 'Guillaume Le Breton, Fabien Rondepierre, Maxime Fery and Oriane Bonhomme'

# The full version, including alpha/beta/rc tags
release = '1.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# root_doc = 'index'
master_doc = 'index'

extensions = ['recommonmark','sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel', 'sphinx.ext.extlinks', 'sphinx.ext.napoleon', 'sphinxcontrib.bibtex']

bibtex_bibfiles = ['biblio.bib']
bibtex_default_style = 'unsrt'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_logo = '_static/alpaga_logo.svg'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

rst_prolog = """
 .. include:: <s5defs.txt>
 .. |alpaga_DOI| replace:: 10.5281/zenodo.5639392

"""

extlinks = {
    'alpaga_zenodo': ('https://zenodo.org/record/5639393#.Yw8A5fc6-ds/%s', None)
           }


exclude_patterns=['some_advice_to_compile_with_sphnix.txt', 'compile_wiki_for_windows.txt']
