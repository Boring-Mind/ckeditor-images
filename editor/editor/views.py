import imghdr
from os import path
from random import randrange
from typing import Sequence, Dict, Tuple

import nanoid
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render

from .forms import ImageForm
from .models import Article
from editor.editor.images import ImageUpload


# from sys import getsizeof

def editor_view(request):
    return render(request, 'editor.html', {})


def process_article(request):
    title = randrange(10000, 25000)
        
    article_body = request.POST['article_body']

    article = Article(title=title, body=article_body)
    article.save()

    json_response = {'title': str(title)}
    json_response['body'] = article_body
    json_response['world'] = 'Hello World!'
    return JsonResponse(
        json_response, content_type='application/json'
    )


def process_images(request):
    return ImageUpload(request).process_images()


def upload_view(request) -> HttpResponse:
    if request.method == 'POST':
        if request.headers['content_type'] == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif 'multipart/form-data' in request.headers['content_type']:
            return process_images(request)
    else:
        return HttpResponseNotFound()
