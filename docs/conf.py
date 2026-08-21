"""Sphinx configuration for the Romeo technical, teaching and operational portal."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

project = "Romeo"
copyright = "2026, TheBitPoets"
author = "TheBitPoets"
language = "it"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build", "release/runtime-image-current.env"]

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "tasklist"]
myst_heading_anchors = 3

autosummary_generate = True
autodoc_typehints = "description"
autodoc_mock_imports = ["adafruit_crickit", "board", "picamera2", "pygame"]

html_theme = "furo"
html_title = "Romeo · TheBitLab"
html_show_sourcelink = True
