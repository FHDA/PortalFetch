# PortalFetch

[![CircleCI](https://circleci.com/gh/FHDA/PortalFetch.svg?style=svg)](https://circleci.com/gh/FHDA/PortalFetch)  

## Information

This tool/project fetch data from De Anza College / Foothill College portal and save to json file
This is Emily's test.
## Requirements

Python v3.6
node v10.16.0
npm v6.9.0 or above

## Install

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```script
pip install -r requirements.txt
```

## Usage(@todo)

Activate your virtual environment if you have. Usually the command is `activate virtural_name`

## Development (@todo)

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```py
npm install
pip install -r requirements.txt
```
  
We require all contributor write docsting for other contributors easy to follow.  
One of software development process is TDD. We highly recommended you *write test before code*  
However, test is not require but recommended.  
The philosophy is **you must know exactly the detailed behavior of your code doing**.  

We use [pytest](https://docs.pytest.org/) to test our code.  
We use [pydocstring](http://pydocstyle.org/) to test our docstring.  
We use [autopep8](https://github.com/hhatto/autopep8) to formating our code.  
We use [pylint](https://pylint.org) as Python linter.  

## Coding Style

In general, we follow PEP8 Python coding style and Google pyguide
However, if PEP8 and Google pyguide has conflict style, PEP8 take place.

Some special rule:

1. max-line-length: 100

Please also write docstring for contributor easy to follow.
We follow Google docstring style(https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

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
    ├── scripts/  
    │   ├── pre-commit.sh  
    │   └── pre-push.sh  
    ├── tests/  
    │   ├── 00_empty_test.py  
    │   └── PortalFetch  
    │       ├── helpers_tests.py  
    │       └── PortalFetch_tests.py  
    │  
    ├── .gittattributes
    ├── .gitignore
    ├── package.json
    ├── pylintrc
    ├── requirements.txt  
    ├── setup.cfg  
    ├── LICENSE  
    └── README.md 

## Git Commit message

In general, we use "Semantic Commit Messages"

Reference:

1. https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716
2. https://github.com/joelparkerhenderson/git_commit_message#begin-with-a-short-summary-line
