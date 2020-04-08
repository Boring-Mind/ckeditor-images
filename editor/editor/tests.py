import os
import json
import re
from typing import BinaryIO
import unittest
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from editor.editor.image_process import ImageProcess


class TestHelperMethods():
    """Contains all the methods, needed in both integrate and unit tests."""

    @classmethod
    def get_test_image_path(cls, img_name: str) -> str:
        """Get path to the image in the test folder."""
        img_folder = os.path.join(settings.MEDIA_ROOT, 'test_img')
        return os.path.join(img_folder, img_name)


class IntegrationTests(TestCase):
    # -----------------------------------------
    # HELPER METHODS
    
    # -----------------------------------------
    # Post images
    # -----------------------------------------

    def post_image(self, image: BinaryIO) -> dict:
        response = self.client.post('/upload/', {
            'upload': image
        })
        return json.loads(response.content)

    def open_image_and_post_it(self, image_name: str) -> dict:
        """Open an image with the given name, post it and get a parsed json response.
        
        Output will be the same as in the post_image function:
        dict object with json response content.
        """
        path = TestHelperMethods.get_test_image_path(image_name)
        with open(path, 'rb') as image:
            response = self.post_image(image)
        return response

    # -----------------------------------------
    # Working with responses
    # -----------------------------------------

    def get_error_from_response(self, response) -> str:
        """Get an error message from received jsonreponse."""
        return response['error']['message']

    # -----------------------------------------
    # CASES
    # 
    # Description:
    # 1. Needed to reduce code duplication
    # 2. Always contains assert statement

    def case_check_received_url(self, response_url: str):
        """If the url in the response is not correct, raise an AssertError.

        Filename must be something like this: 7gXL4258iz7ePBG.jpg
        And that requirement is satisfied by a regex part.
        """
        ref_url = ("http://127.0.0.1:8000/media/uploads/"
                   r"[\w-]{15}\.\w{3,4}")
        match = re.fullmatch(ref_url, response_url)
        self.assertTrue(
            match is not None,
            "Image url received from the response is not correct.\n"
            f"Received url: {response_url}"
        )

    # -----------------------------------------
    # TESTS

    def test_return_404_on_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 404)

    @unittest.expectedFailure
    def test_failed_response_doesnt_contain_img_url(self):
        img_path = TestHelperMethods.get_test_image_path('html_page.jpg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
            
        # There cannot be an urls in a failed request
        self.assertTrue('url' not in response)
        self.assertTrue('urls' not in response)

    def test_return_filenames_on_success_image_upload(self):
        response = self.open_image_and_post_it('image.jpg')
        response_url = response['url']

        self.case_check_received_url(response_url)

    @unittest.expectedFailure
    def test_return_correct_error_on_failed_image_upload(self):
        img_path = TestHelperMethods.get_test_image_path('icon.svg')

        with open(img_path, 'rb') as image:
            response = self.post_image(image)
        error = self.get_error_from_response(response)

        ref_error = (
            'Unsupported image type. '
            'We can handle only jpg, png, gif, webp, tiff.'
        )
        self.assertEqual(ref_error, error)

    def test_success_response_doesnt_contain_err_message(self):
        response = self.open_image_and_post_it('image.jpg')
        # There cannot be an error message in a successful request
        self.assertTrue('error' not in response)


class UnitTests(TestCase):
    # -----------------------------------------
    # HELPER METHODS
    # 
    # Description:
    # 1. Needed to reduce code duplication
    # 2. They usually are class methods, and get cls argument instead of self
    
    # -----------------------------------------
    # Working with filesystem
    # -----------------------------------------
    @classmethod
    def split_filename(cls, filename: str):
        filename, ext = os.path.splitext(filename)
        if ext == '':
            filename, ext = ext, filename
        return (filename, ext)

    @classmethod
    def fullmatch_filename(cls, filename: str, ext: str):
        """Return match object if the filename fits to the regex, or None if not.

        Example of the filename param:
        'simple.jpg'

        Example of the ext param:
        '.jpg'
        """
        return re.fullmatch(r"[\w-]{15}" + ext, filename)
    
    @classmethod
    def get_extension(cls, filename: str) -> str:
        """Return file extension.
        
        Example of the filename param:
        'simple.jpg'
        
        Example of the return value:
        '.jpg'
        """
        return UnitTests.split_filename(filename)[1]

    @classmethod
    def path_to_test_img(cls, img_name: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'test_img', img_name)

    # -----------------------------------------
    # CASES
    # 
    # Description:
    # 1. Needed to reduce code duplication
    # 2. Always contains assert statement

    def case_filename_check(self, filename: str):
        """Raise AssertException if the filename is not correct.
        
        Example of the filename param:
        'simple.jpg'

        Correct filename would be:
        '2ZxeY-Fqr_TZBx0.jpg'
        """
        img_name = ImageProcess(filename).filename

        ext = UnitTests.get_extension(img_name)
        match = UnitTests.fullmatch_filename(img_name, ext)
        self.assertNotEqual(match, None, f'Result is: {img_name}')

    def case_check_image(self, expected_result: str, img_name: str):
        path = UnitTests.path_to_test_img(img_name)

        # print(dir())
        with patch(
            'editor.editor.tests.ImageProcess.generate_path',
            return_value=path
        ):
            instance = ImageProcess(img_name)
            actual_result = instance.check_image()
            instance.generate_path.assert_called()

        self.assertEqual(expected_result, actual_result)

    def case_image_not_exists(self, img_name: str):
        img_path = UnitTests.path_to_test_img(img_name)
        message = (f'Unable to open image: \'{img_path}\': '
                   'No such file or directory')
        self.case_check_image(message, img_name)
    
    # -----------------------------------------
    # TESTS

    def test_filename_check(self):
        self.case_filename_check('simple.jpg')
        self.case_filename_check('simple.jpeg')
        self.case_filename_check('simple.png')
        self.case_filename_check('simple.giff')
        self.case_filename_check('simple.webp')
        self.case_filename_check('simple.tiff')
        self.case_filename_check('.jpg')
        self.case_filename_check('.vsd..sd.v.sdv.jpg')

    def test_filepath_check(self):
        img_name = 'image.jpg'

        # We are testing only path to the file
        # So we don't need the filename
        # Which is set by random with py-nanoid lib
        ref_path = os.path.join(settings.UPLOAD_ROOT, img_name)
        ref_path = os.path.split(ref_path)[0]

        tested_path = ImageProcess.generate_path(img_name)
        tested_path = os.path.split(tested_path)[0]

        self.assertEqual(tested_path, ref_path)

    def test_check_image(self):
        self.case_check_image('Image check completed', 'image.jpg')
        self.case_check_image('Image check completed', 'image.png')
        self.case_check_image('Image check completed', 'image.webp')
        self.case_check_image('Image check completed', 'image.tiff')
        self.case_check_image('Image check completed', 'image.gif')

        # self.case_check_image(
        #     'File is too large. Maximum allowed size is 2.5Mb', 'large.jpg'
        # )

        self.case_check_image('Unsupported mime type', 'html_page.jpg')
        self.case_check_image('Unsupported mime type', 'malicious_js.png')
        self.case_check_image('Unsupported mime type', 'icon.svg')

        self.case_image_not_exists('false_name.none')
        self.case_image_not_exists('images.jpg')
        self.case_image_not_exists('image.jpg1')
        self.case_image_not_exists('image.jpg.jpg')

    def test_image_url(self):
        """Test image url generation."""
        impr_instance = ImageProcess('simple.jpg')
        img_name = impr_instance.filename
        ref_url = f'http://127.0.0.1:8000/media/uploads/{img_name}'

        tested_url = impr_instance.generate_img_url()

        self.assertEqual(tested_url, ref_url)
