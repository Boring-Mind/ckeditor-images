# ckeditor-images
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

## Requirements
* Python 3.6 - needed for f-string syntax


Another requirements are listed in requirements.txt
