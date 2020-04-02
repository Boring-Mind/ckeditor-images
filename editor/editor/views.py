import nanoid
from os import path
from random import randrange
# from sys import getsizeof
import imghdr

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

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


def generate_name(filename: str) -> str:
    """Generate filename for new image.

    Resulted filename looks like that: nMcsadvknv.jpg
    """
    extension = path.splitext(filename)[1]
    if extension == '':
        extension = filename
    new_name = nanoid.generate(size=15)
    return new_name + extension


def generate_path(filename: str) -> str:
    """Generate absolute path to new image."""
    return path.join(settings.UPLOAD_ROOT, filename)


def generate_img_url(filename: str) -> str:
    """Generate url link to the new image."""
    return settings.MEDIA_URL + '/uploads/' + filename


def get_unique_filename(filename: str) -> str:
    """Check generated filename for uniqueness."""
    new_name = generate_name(filename)
    new_path = generate_path(new_name)

    while path.exists(new_path):
        new_path = generate_path(new_name)

    return new_name


def check_image(image_path: str) -> str:
    """Test image for the correct filetype."""
    if not path.exists(image_path):
        return (f'Unable to open image: \'{image_path}\': '
                'No such file or directory')

    img_type = imghdr.what(image_path)
    if img_type in settings.SUPPORTED_IMG_FORMATS:
        return ''
    
    return 'Unsupported mime type'


def get_image_data(request):
    image = request.FILES['upload']
    filename = request.FILES['upload'].name

    filename = get_unique_filename(filename)
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
        return HttpResponse(status=404)
