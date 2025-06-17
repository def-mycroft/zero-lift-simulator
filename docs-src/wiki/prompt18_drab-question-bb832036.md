# prompt18 - introduce auto docs drab-question bb832036

random codename: drab-question bb832036

#prompt 

***




Create a minimal setup for Sphinx that generates a static documentation
site from Python docstrings using the Furo theme. It should:

1. Initialize a Sphinx project with a clean structure.
2. Enable extensions for autodoc and napoleon (to parse Google/numpydoc).
3. Set the theme to Furo.
4. Automatically include documentation for all modules in the current
   Python package.
5. Support Markdown parsing for custom pages using myst-parser.

You should output a script or Makefile commands that:
- Initializes the docs folder
- Adds the needed config values to conf.py
- Autogenerates the .rst or .md files with autodoc
- Builds the HTML site in _build/html

also, add to zero-liftsim cli an option `dev --build-docs`, which should build these docs. 

also, keep in mind that I want to browse this via gh pages and make it public. 

also, don't interfere with the current "docs/", that is something different than mere technical docs. I should be able to add md documents from here to a toc and view them w/ gh pages 

