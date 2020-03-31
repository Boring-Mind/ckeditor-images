import nanoid
from os import path
from random import randrange
# from sys import getsizeof

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from wand.image import Image
from wand.exceptions import BlobError, FileOpenError

from .models import Article
from .forms import ImageForm


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


def check_image(image_path: str) -> str:
    try:
        with Image(filename=image_path):
            # Image is correct
            return ''
    except BlobError:
        return (f'Unable to open image: \'{image_path}\': '
                'No such file or directory')
    except FileOpenError:
        return 'Unsupported mime type'


def get_image_data(request):
    image = request.FILES['upload']
    filename = request.FILES['upload'].name

    filename = get_new_filename(filename)
    image.name = filename

    if check_image(image.name):
        return {'image': image}
    else:
        return {}


def save_image_to_db(request) -> bool:
    form = ImageForm(request.POST, get_image_data(request))
    if form.is_valid():
        form.save()
        return True
    else:
        return False


def process_images(request) -> HttpResponse:
    # print(request.FILES["upload"].size)

    if save_image_to_db(request) is True:
        return HttpResponse('Image was received')
    else:
        return HttpResponse('Some error was occured')


def upload_view(request) -> HttpResponse:
    if request.method == 'POST':
        if request.headers['content_type'] == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif 'multipart/form-data' in request.headers['content_type']:
            return process_images(request)
    else:
        return HttpResponse('<h1>GET was sent, but POST needed</h1>')
