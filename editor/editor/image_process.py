import imghdr
import os

import nanoid
from django.conf import settings

from editor.webutils.urlutils import URLUtils


class StatusMessages():
    OK = ''
    FILE_NOT_FOUND = 'File is already deleted or was not existed.'
    INVALID_FILETYPE = 'Unsupported image type. We can handle jpg, png, gif, webp, tiff.'
    IMAGE_TOO_LARGE = 'Image is too big (max 1.5MB).'


class ImageProcess:
    def __init__(self, filename: str):
        self.__filename = ''
        self.filename = self.get_unique_filename(filename)

    # Filename property
    ###################################################
    def _get_filename(self):
        return self.__filename

    def _set_filename(self, filename: str) -> bool:
        try:
            self.__filename = filename
            return True
        except Exception:
            return False

    filename = property(_get_filename, _set_filename)
    ###################################################

    @classmethod
    def generate_name(cls, filename: str) -> str:
        """Generate filename for new image.

        Resulted filename looks like that: nMcsadvknv.jpg
        """
        extension = os.path.splitext(filename)[1]
        if extension == '':
            extension = filename
        new_name = nanoid.generate(size=15)

        return new_name + extension

    @classmethod
    def generate_path(cls, filename: str) -> str:
        """Generate absolute path to new image."""
        return os.path.join(settings.UPLOAD_ROOT, filename)

    def get_unique_filename(self, filename: str) -> str:
        """Check generated filename for uniqueness."""
        new_name = ImageProcess.generate_name(filename)
        new_path = ImageProcess.generate_path(new_name)

        if os.path.exists(new_path):
            new_path = ImageProcess.generate_path(new_name)

        self.filename = new_name
        return new_name

    def remove_image(self) -> bool:
        """Remove image file after unsuccessful check."""
        try:
            os.remove(self.generate_path(self.filename))
            return True
        except OSError:
            return False

    def generate_img_url(self) -> str:
        """Generate relative url link to the new image."""
        domain = URLUtils.get_current_domain()
        filename = self.filename
        return (
            f'http://{domain}{settings.MEDIA_URL}uploads/{filename}'
        )

    def check_image(self) -> str:
        """Test image for the correct filetype."""
        image_path = ImageProcess.generate_path(self.filename)
        if not os.path.isfile(image_path):
            # logging.error(f'Unable to open image: \'{image_path}\': '
            #         'No such file or directory')
            self.remove_image()
            return StatusMessages.FILE_NOT_FOUND

        img_type = imghdr.what(image_path)
        if img_type in settings.SUPPORTED_IMG_FORMATS:
            # logging.error('Unsupported mime type of image')
            return StatusMessages.OK

        # logging.info('Image check completed')
        self.remove_image()
        return StatusMessages.INVALID_FILETYPE
