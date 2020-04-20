from random import randrange

from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from editor.editor.images import ImageUpload
from editor.editor.models import Article
from editor.webutils.responses import HttpResponseCodes


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
    content_length = int(request.headers.get('Content-Length'))
    if content_length < settings.MAXIMUM_UPLOAD_SIZE:
        return ImageUpload(request).process_images()
    else:
        return HttpResponseCodes.payload_too_large()


def upload_view(request) -> HttpResponse:
    if request.method == 'POST':
        if request.headers.get('content_type') == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif 'multipart/form-data' in request.headers.get('content_type'):
            return process_images(request)
    else:
        return HttpResponseNotFound()
