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


# def generate_name(filename: str) -> str:
#     """Generate filename for new image.

#     Resulted filename looks like that: nMcsadvknv.jpg
#     """
#     extension = path.splitext(filename)[1]
#     if extension == '':
#         extension = filename
#     new_name = nanoid.generate(size=15)
#     return new_name + extension


# def generate_path(filename: str) -> str:
#     """Generate absolute path to new image."""
#     return path.join(settings.UPLOAD_ROOT, filename)


# def get_current_domain():
#     current_site = Site.objects.get_current()
#     return current_site.domain


# def generate_img_url(filename: str) -> str:
#     """Generate relative url link to the new image."""
#     domain = get_current_domain()
#     return 'http://' + domain + settings.MEDIA_URL + 'uploads/' + filename


# def get_unique_filename(filename: str) -> str:
#     """Check generated filename for uniqueness."""
#     new_name = generate_name(filename)
#     new_path = generate_path(new_name)

#     while path.exists(new_path):
#         new_path = generate_path(new_name)

#     return new_name


# def check_image(image_path: str) -> str:
#     """Test image for the correct filetype."""
#     if not path.isfile(image_path):
#         # logging.error(f'Unable to open image: \'{image_path}\': '
#         #         'No such file or directory')
#         return (f'Unable to open image: \'{image_path}\': '
#                 'No such file or directory')

#     img_type = imghdr.what(image_path)
#     if img_type in settings.SUPPORTED_IMG_FORMATS:
#         # logging.info('Image check completed')
#         return 'Image check completed'
    
#     # logging.error('Unsupported mime type of image')
#     return 'Unsupported mime type'


# def get_image_data(request) -> Sequence[Tuple[Dict, str]]:
#     image = request.FILES['upload']
#     filename = request.FILES['upload'].name

#     filename = get_unique_filename(filename)
#     image.name = filename

#     if check_image(image.name):
#         return ({'image': image}, filename)
#     else:
#         raise ValidationError


# def save_image_to_db(request) -> bool:
#     image_data, image_name = get_image_data(request)

#     form = ImageForm(request.POST, image_data)
#     if form.is_valid():
#         form.save()
#         img_url = generate_img_url(image_name)
#         return {'url': img_url}
#     else:
#         raise ValidationError


def process_images(request):
    # print(request.FILES["upload"].size)

    return ImageUpload(request).process_images()

    # try:
    #     response = save_image_to_db(request)
    #     return JsonResponse(response)
    # except ValidationError:
    #     return HttpResponseServerError()


def upload_view(request) -> HttpResponse:
    if request.method == 'POST':
        if request.headers['content_type'] == 'application/x-www-form-urlencoded':
            return process_article(request)
        elif 'multipart/form-data' in request.headers['content_type']:
            return process_images(request)
    else:
        return HttpResponseNotFound()
