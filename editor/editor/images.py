from typing import Sequence, Dict, Tuple

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from editor.editor.forms import ImageForm
from editor.editor.image_process import ImageProcess, StatusMessages


class ImageUpload():
    def __init__(self, request):
        self.request = request
        self.impr_instance = None

    def get_image_data(self) -> Sequence[Tuple[Dict, str]]:
        image = self.request.FILES['upload']
        filename = self.request.FILES['upload'].name

        self.impr_instance = ImageProcess(filename)
        image.name = self.impr_instance.filename

        return ({'image': image}, filename)

    def save_image_to_db(self):
        image_data, image_name = self.get_image_data()

        form = ImageForm(self.request.POST, image_data)
        if form.is_valid():
            form.save()

            img_status = self.impr_instance.check_image()
            if img_status == StatusMessages.OK:
                result_url = self.impr_instance.generate_img_url()
                return {'url': result_url}
            else:
                return {'error': {'message': img_status}}
        
        # Add function to cleanup form data from server
        # self.impr_instance.remove_image()

        raise ValidationError('Invalid data in the Image form')

    def process_images(self):
        response = self.save_image_to_db()
        return JsonResponse(response)
