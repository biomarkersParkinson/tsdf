# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'tsdf'
copyright = '2024, Netherlands eScience Center'
author = 'Netherlands eScience Center'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# General configuration
extensions = [
    "myst_nb",
    "autoapi.extension",
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
autoapi_dirs = ['../src']
autoapi_add_toctree_entry = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': 'https://biomarkersparkinson.github.io/tsdf/',
}

html_static_path = ['_static']

# Keep the main TOC always visible
html_sidebars = {
    '**': [
        'globaltoc.html',  # Add this line
        'relations.html',  # needs 'show_related': True theme option to display
        'sourcelink.html',
        'searchbox.html',
    ]
}

# Repository settings
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "biomarkersParkinson",  # Username
    "github_repo": "tsdf",  # Repo name
    "github_version": "main",  # Version
    "conf_py_path": "/docs/",  # Path in the checkout to the docs root
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
