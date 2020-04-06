import imghdr
from os import path
from typing import Sequence, Dict, Tuple

import nanoid
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseServerError

from editor.editor.forms import ImageForm
from editor.editor.image_process import ImageProcess


class ImageUpload():
    def __init__(self, request):
        # self.image_name = ''
        self.request = request

    def get_current_domain(self):
        current_site = Site.objects.get_current()
        return current_site.domain

    def generate_img_url(self, filename: str) -> str:
        """Generate relative url link to the new image."""
        domain = self.get_current_domain()
        return 'http://' + domain + settings.MEDIA_URL + 'uploads/' + filename

    def check_image(self, image_path: str) -> str:
        """Test image for the correct filetype."""
        if not path.isfile(image_path):
            # logging.error(f'Unable to open image: \'{image_path}\': '
            #         'No such file or directory')
            return (f'Unable to open image: \'{image_path}\': '
                    'No such file or directory')

        img_type = imghdr.what(image_path)
        if img_type in settings.SUPPORTED_IMG_FORMATS:
            # logging.info('Image check completed')
            return 'Image check completed'
            
        # logging.error('Unsupported mime type of image')
        return 'Unsupported mime type'

    def get_image_data(self) -> Sequence[Tuple[Dict, str]]:
        image = self.request.FILES['upload']
        filename = self.request.FILES['upload'].name

        filename = ImageProcess.get_unique_filename(filename)
        image.name = filename

        if self.check_image(image.name):
            return ({'image': image}, filename)
        else:
            raise ValidationError

    def save_image_to_db(self):
        image_data, image_name = self.get_image_data()

        form = ImageForm(self.request.POST, image_data)
        if form.is_valid():
            form.save()
            result_url = self.generate_img_url(image_name)
            return {'url': result_url}
        else:
            raise ValidationError

    def process_images(self):
        try:
            response = self.save_image_to_db()
            return JsonResponse(response)
        except ValidationError:
            return HttpResponseServerError()
