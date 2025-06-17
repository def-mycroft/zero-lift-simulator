import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

project = 'Zero Lift Simulator'
author = 'Zero Lift'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]

html_theme = 'furo'

source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']

