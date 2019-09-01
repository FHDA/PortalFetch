# PortalFetch

## Information

This tool/prject fetch data from De Anza College / Foothill College portal and save to json file

## Coding Style

In general, we follow PEP8 Python coding style and Google pyguide
However, if PEP-8 and Google pyguide has conflict style, PEP8 take place.

Some special rule:

1. max-line-length: 100

Reference:

1. https://www.python.org/dev/peps/pep-0008/
2. http://google.github.io/styleguide/pyguide.html

## Project Structure

    .
    PortalFetch/  
    │  
    ├── bin/  
    │  
    ├── docs/  
    │   └── docs.md  
    │  
    ├── PortalFetch/  
    │   ├── __init__.py  
    │   ├── runner.py  
    │   └── PortalFetch/  
    │       ├── __init__.py  
    │       ├── helpers.py  
    │       └── PortalFetch.py  
    │  
    ├── data/  
    │   └── input.json  
    │  
    ├── tests/  
    │   └── PortalFetch  
    │       ├── helpers_tests.py  
    │       └── PortalFetch_tests.py  
    │  
    ├── .gitignore  
    ├── LICENSE  
    └── README.md  

## Git Commit message

In general, we use "Semantic Commit Messages"

Reference:

1. https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716
2. https://github.com/joelparkerhenderson/git_commit_message#begin-with-a-short-summary-line
