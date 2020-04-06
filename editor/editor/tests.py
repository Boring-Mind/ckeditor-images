import os
import json
import re
from typing import BinaryIO
import unittest

from django.conf import settings
from django.http.request import HttpRequest
from django.test import TestCase

import editor.editor.views as views
from editor.editor.images import ImageUpload
from editor.editor.image_process import ImageProcess


class ImageLoadTest(TestCase):
    def get_image_path(self, img_name: str) -> str:
        """Get path to the image in the test folder."""
        img_folder = os.path.join(settings.MEDIA_ROOT, 'test_img')
        return os.path.join(img_folder, img_name)
    
    def post_image(self, image: BinaryIO) -> dict:
        response = self.client.post('/upload/', {
            'upload': image
        })
        return json.loads(response.content)

    def load_image_to_the_server(self, image_name: str) -> dict:
        img_path = self.get_image_path(image_name)

        with open(img_path, 'rb') as image:
            response = self.post_image(image)

        return response

    def compare_with_reference(self, response_url: str) -> bool:
        """Reference url is a regex string.

        Filename must be something like this: 7gXL4258iz7ePBG.jpg
        And that requirement is satisfied by a regex part.
        """
        ref_url = ("http://127.0.0.1:8000/media/uploads/"
                   r"[\w-]{15}\.\w{3,4}")
        match = re.fullmatch(ref_url, response_url)
        return match is not None

    def test_return_error_on_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 404)

    def test_success_response_doesnt_contain_err_message(self):
        img_path = self.get_image_path('image.jpg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
            
        # There cannot be an error message in a successful request
        self.assertTrue('error' not in response)

    @unittest.expectedFailure
    def test_failed_response_doesnt_contain_img_url(self):
        img_path = self.get_image_path('html_page.jpg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
            
        # There cannot be an urls in a failed request
        self.assertTrue('url' not in response)
        self.assertTrue('urls' not in response)

    def test_return_filenames_on_success_image_upload(self):
        img_path = self.get_image_path('image.jpg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
        response_url = response['url']

        self.assertTrue(
            self.compare_with_reference(response_url),
            "Url received from the response doesn't match to the reference.\n"
            f"Received url: {response_url}"
        )

    def get_error_from_response(self, response) -> str:
        return response['error']['message']

    @unittest.expectedFailure
    def test_return_correct_error_on_failed_image_upload(self):
        img_path = self.get_image_path('icon.svg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
        error = self.get_error_from_response(response)

        ref_error = (
            'Unsupported image type. '
            'We can handle only jpg, png, gif, webp, tiff.'
        )
        self.assertEqual(ref_error, error)


class ImageProcessTest(TestCase):
    def filename_is_correct(self, filename: str, ext: str):
        test_filename = ImageProcess.generate_name(filename + ext)
        match = re.fullmatch(r"[\w-]{15}" + ext, test_filename)
        self.assertNotEqual(match, None, f'Result is: {test_filename}')

    def make_img_path(self, img_name: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'test_img', img_name)

    def get_error_message_from_response(self, response: dict) -> str:
        return response['error']['message']

    def image_checking_case(self, message: str, img_name: str):
        upload = ImageUpload(HttpRequest())
        img_path = self.make_img_path(img_name)

        result = upload.check_image(img_path)

        self.assertEqual(message, result)

    def image_checking_not_exists_case(self, img_name: str):
        img_path = self.make_img_path(img_name)
        message = (f'Unable to open image: \'{img_path}\': '
                   'No such file or directory')
        self.image_checking_case(message, img_name)


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

        tested_path = ImageProcess.generate_path(img_name)
        tested_path = os.path.split(tested_path)[0]

        self.assertEqual(tested_path, ref_path)

    def test_image_checking(self):
        self.image_checking_case('Image check completed', 'image.jpg')
        self.image_checking_case('Image check completed', 'image.png')
        self.image_checking_case('Image check completed', 'image.webp')
        self.image_checking_case('Image check completed', 'image.tiff')
        self.image_checking_case('Image check completed', 'image.gif')

        # self.image_checking_case(
        #     'File is too large. Maximum allowed size is 2.5Mb', 'large.jpg'
        # )

        self.image_checking_case('Unsupported mime type', 'html_page.jpg')
        self.image_checking_case('Unsupported mime type', 'malicious_js.png')
        self.image_checking_case('Unsupported mime type', 'icon.svg')

        self.image_checking_not_exists_case('false_name.none')
        self.image_checking_not_exists_case('images.jpg')
        self.image_checking_not_exists_case('image.jpg1')
        self.image_checking_not_exists_case('image.jpg.jpg')

    def test_image_url(self):
        """Test image url generation."""
        # upload = ImageUpload(HttpRequest())
        filename = 'simple.jpg'
        ref_url = 'http://127.0.0.1:8000/media/uploads/' + filename

        tested_url = ImageProcess.generate_img_url(filename)

        self.assertEqual(tested_url, ref_url)
