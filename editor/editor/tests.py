import os
import json
import re
from io import BytesIO
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from editor.editor.image_process import ImageProcess, StatusMessages
from editor.webutils.urlutils import URLUtils


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

    def post_image(self, image: BytesIO) -> dict:
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

    def get_error_from_response(self, response: dict) -> str:
        """Get an error message from received jsonresponse."""
        return response['error']['message']

    # -----------------------------------------
    # Working with files
    # -----------------------------------------

    def file_cleanup(self, response: dict):
        """Parse filename from the received url and remove the file.

        Needed in order to cleanup uploads folder from the test images.
        Must be called after every tests, that are saving correct images.
        """
        if 'url' in response:
            filename = URLUtils.get_filename_from_url(response['url'])
            path = ImageProcess.generate_path(filename)
            os.remove(path)

    # -----------------------------------------
    # Generate random data
    # -----------------------------------------

    def get_long_byte_string(self, length: str) -> BytesIO:
        """Generate random string of bytes with given length.

        length cannot be larger than 1000 and lower than zero.
        """
        return os.urandom(length)

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

    def case_send_post_request_with_length(self, length: int) -> dict:
        """Send POST request with given length.

        Length cannot be more than 1000 or smaller than zero.
        """
        data = self.get_long_byte_string(length)
        return self.client.post('/upload/', {
            'upload': BytesIO(data)
        })

    # -----------------------------------------
    # TESTS

    def test_return_404_on_get_request(self):
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 404)

    def test_failed_response_does_not_contain_img_url(self):
        response = self.open_image_and_post_it('html_page.jpg')
            
        # There cannot be an urls in a failed request
        self.assertTrue('url' not in response)
        self.assertTrue('urls' not in response)

    def test_return_filenames_on_success_image_upload(self):
        response = self.open_image_and_post_it('image.jpg')
        response_url = response['url']

        self.case_check_received_url(response_url)

        self.file_cleanup(response)

    def test_return_correct_error_on_failed_image_upload(self):
        response = self.open_image_and_post_it('icon.svg')
        error = self.get_error_from_response(response)

        ref_error = (
            'Unsupported image type. '
            'We can handle jpg, png, gif, webp, tiff.'
        )
        self.assertEqual(ref_error, error)

    def test_success_response_doesnt_contain_err_message(self):
        response = self.open_image_and_post_it('image.jpg')
        # There cannot be an error message in a successful request
        self.assertTrue('error' not in response)

        self.file_cleanup(response)

    def test_image_is_deleted_after_failed_upload(self):
        with patch(
            'editor.editor.tests.ImageProcess.get_unique_filename',
            return_value='wrong_file.ext'
        ):
            self.open_image_and_post_it('icon.svg')
        
        file_exists = os.path.isfile(
            ImageProcess.generate_path('wrong_file.ext')
        )
        self.assertFalse(file_exists)

    def test_image_exists_after_successful_upload(self):
        # Patch is used because image name is generated by random.
        # But we must be able to test, whether new image file exists or not.
        with patch(
            'editor.editor.tests.ImageProcess.get_unique_filename',
            return_value='correct_file.ext'
        ):
            response = self.open_image_and_post_it('image.gif')
        
        file_exists = os.path.isfile(
            ImageProcess.generate_path('correct_file.ext')
        )
        self.assertTrue(file_exists)

        self.file_cleanup(response)

    def test_long_requests_are_refused(self):
        """Requests, larger than the maximum upload size are accepted."""
        length = settings.MAXIMUM_UPLOAD_SIZE
        
        response = self.case_send_post_request_with_length(length)

        self.assertEqual(response.status_code, 413)

    def test_small_requests_are_accepted(self):
        """Requests, smaller than the maximum upload size are accepted."""
        length = settings.MAXIMUM_UPLOAD_SIZE - 1024
        
        response = self.case_send_post_request_with_length(length)

        self.assertNotEqual(response.status_code, 413)


class UnitTests(TestCase):
    
    def setUp(self):
        """Mock some functions from the ImageProcess class
        and add cleanup for them.
        """
        mock_remove = patch(
            'editor.editor.tests.ImageProcess.remove_image',
            return_value=True
        ).start()
        self.addCleanup(patch.stopall)

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

    def case_check_image(self, img_name: str, expected_result: str):
        path = UnitTests.path_to_test_img(img_name)

        with patch(
            'editor.editor.tests.ImageProcess.generate_path',
            return_value=path
        ):
            instance = ImageProcess(img_name)
            actual_result = instance.check_image()
            instance.generate_path.assert_called()

        self.assertEqual(expected_result, actual_result)
    
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
        # Upload valid images
        self.case_check_image('image.jpg', StatusMessages.OK)
        self.case_check_image('image.png', StatusMessages.OK)
        self.case_check_image('image.webp', StatusMessages.OK)
        self.case_check_image('image.tiff', StatusMessages.OK)
        self.case_check_image('image.gif', StatusMessages.OK)

        # self.case_check_image(
        #     'File is too large. Maximum allowed size is 2.5Mb', 'large.jpg'
        # )

        # Upload images with unsupported mime type
        self.case_check_image('html_page.jpg', StatusMessages.INVALID_FILETYPE)
        self.case_check_image('malicious_js.png', StatusMessages.INVALID_FILETYPE)
        self.case_check_image('icon.svg', StatusMessages.INVALID_FILETYPE)

        # Upload non-existing image files
        self.case_check_image('false_name.none', StatusMessages.FILE_NOT_FOUND)
        self.case_check_image('images.jpg', StatusMessages.FILE_NOT_FOUND)
        self.case_check_image('image.jpg1', StatusMessages.FILE_NOT_FOUND)
        self.case_check_image('image.jpg.jpg', StatusMessages.FILE_NOT_FOUND)

    def test_image_url(self):
        """Test image url generation."""
        impr_instance = ImageProcess('simple.jpg')
        img_name = impr_instance.filename
        ref_url = f'http://127.0.0.1:8000/media/uploads/{img_name}'

        tested_url = impr_instance.generate_img_url()

        self.assertEqual(tested_url, ref_url)
