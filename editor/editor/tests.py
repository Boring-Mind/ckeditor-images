import os
import re

from django.test import TestCase
from django.conf import settings

import editor.editor.views as views


class ImageLoad(TestCase):
    def get_image_path(self, img_name: str) -> str:
        """Get path to the image in the test folder."""
        img_folder = os.path.join(settings.MEDIA_ROOT, 'test_img')
        return os.path.join(img_folder, img_name)

    def test_return_error_on_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 404)

    # def test_return_filenames_on_success_image_upload(self):
    #     img_path = self.get_image_path('simple.jpg')

    #     with open(img_path, 'rb') as image:
    #         response = self.client.post('/upload/', {
    #             'upload': image
    #         })
    #         self.assertEqual(response.content, {
    #             "url": "https://example.com/images/foo.jpg"
    #         })


class ImageProcess(TestCase):
    def filename_is_correct(self, filename: str, ext: str):
        test_filename = views.get_new_filename(filename + ext)
        match = re.fullmatch(r"[\w-]{15}" + ext, test_filename)
        self.assertNotEqual(match, None, f'Result is: {test_filename}')

    def test_filename_is_correct(self):
        self.filename_is_correct('simple', '.jpg')
        self.filename_is_correct('simple', '.jpeg')
        self.filename_is_correct('simple', '.png')
        self.filename_is_correct('simple', '.gif')
        self.filename_is_correct('simple', '.webp')
        self.filename_is_correct('simple', '.tiff')
        self.filename_is_correct('', '.jpg')
        self.filename_is_correct('.vsd..sd.v.sdv', '.jpg')
