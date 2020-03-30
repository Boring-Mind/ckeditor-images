import nanoid
from os import path
from random import randrange
from sys import getsizeof

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import Article


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


def get_new_filename(filename: str) -> str:
    extension = path.splitext(filename)[1]
    new_name = nanoid.generate(size=15)
    return new_name + extension


def get_new_filepath(filename: str) -> str:
    filename = get_new_filename(filename)
    return path.join(settings.UPLOAD_ROOT, filename)


def process_images(request) -> HttpResponse:
    filename = request.FILES["upload"].name
    print(get_new_filepath(filename))
    # print(request.FILES["upload"].size)
    return HttpResponse('Image was received')


def upload_view(request) -> HttpResponse:
    if request.method == 'POST':
        if request.headers['content_type'] == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif 'multipart/form-data' in request.headers['content_type']:
            return process_images(request)
    else:
        return HttpResponse('<h1>GET was sent, but POST needed</h1>')
