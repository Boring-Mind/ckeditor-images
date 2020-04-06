import nanoid
from os import path


class ImageProcess:
    def __init__(self):
        pass

    @staticmethod
    def generate_name(filename: str) -> str:
        """Generate filename for new image.

        Resulted filename looks like that: nMcsadvknv.jpg
        """
        extension = path.splitext(filename)[1]
        if extension == '':
            extension = filename
        new_name = nanoid.generate(size=15)
        return new_name + extension
