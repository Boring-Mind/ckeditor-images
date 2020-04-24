# ckeditor-images

[![codecov](https://codecov.io/gh/Boring-Mind/ckeditor-images/branch/master/graph/badge.svg)](https://codecov.io/gh/Boring-Mind/ckeditor-images)
![master](https://github.com/Boring-Mind/ckeditor-images/workflows/master/badge.svg?branch=master)

The app is an example of blog, which supports adding articles with images and embedded videos via the CKEditor5 - WYSIWYG editor.

## Current state:
### The app can:
1. Upload articles and save them in the db
2. Upload images and save them in the upload folder
3. Care about security - large requests are refused, images filetype are checked


## Will be added:
1. Storing image paths in the article model in order to delete images with article
2. Blog page with articles list
3. Detail view of the article

## Used technologies:
#### CI (GitHub Actions):
1. [Snyk](https://snyk.io/) - vulnerability fixer (helps to keep dependencies up-to-date)
2. [PyCharm Python Security Scanner](https://github.com/marketplace/actions/pycharm-python-security-scanner) - Python and Django security checks
3. [Codecov](https://codecov.io/) - Code coverage measurement
4. [Code Inspector](https://github.com/marketplace/code-inspector) - Automated code reviews

## Requirements
* Python 3.6 - needed for f-string syntax


Another requirements are listed in requirements.txt
