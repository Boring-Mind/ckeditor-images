from random import randrange

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

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


def process_images(request):
    request_body = request.POST.body
    print(request_body)
    return HttpResponse('Image was received')


def upload_view(request):
    if request.method == 'POST':
        if request.headers['content_type'] == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif request.headers['content_type'] == 'multipart/form-data':
            return process_images(request)
        
    else:
        return HttpResponse('<h1>GET was sent, but POST needed</h1>')
