from os import path

import nanoid
from django.conf import settings
from editor.webutils.urlutils import URLUtils


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

    def generate_img_url(filename: str) -> str:
        """Generate relative url link to the new image."""
        domain = URLUtils.get_current_domain()
        return (
            'http://' + domain + settings.MEDIA_URL + 'uploads/' + filename
        )
