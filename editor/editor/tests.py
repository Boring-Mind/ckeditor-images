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

    def test_filepath_is_correct(self):
        img_name = 'image.jpg'

        # We are testing only path to the file
        # So we don't need the filename
        # Which is set by random with py-nanoid lib
        ref_path = os.path.join(settings.UPLOAD_ROOT, img_name)
        ref_path = os.path.split(ref_path)[0]

        test_path = views.get_new_filepath(img_name)
        test_path = os.path.split(test_path)[0]

        self.assertEqual(test_path, ref_path)

    def image_checking_case(self, message: str, img_name: str):
        img_path = os.path.join(settings.MEDIA_ROOT, 'test_img', img_name)
        self.assertIn(message, views.check_image(img_path))

    def test_image_checking(self):
        self.image_checking_case('', 'simple.jpg')
        # self.image_checking_case(
        #     'File is too large. Maximum allowed size is 2.5Mb', 'large.jpg'
        # )
        self.image_checking_case('Unsupported mime type', 'html_page.html')
        self.image_checking_case(
            'No such file or directory', 'false_name.none'
        )
