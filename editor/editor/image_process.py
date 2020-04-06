from os import path

import nanoid
from django.conf import settings


class ImageProcess:
    def __init__(self):
        pass

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

    def get_unique_filename(filename: str) -> str:
        """Check generated filename for uniqueness."""
        new_name = ImageProcess.generate_name(filename)
        new_path = ImageProcess.generate_path(new_name)

        while path.exists(new_path):
            new_path = ImageProcess.generate_path(new_name)

        return new_name
