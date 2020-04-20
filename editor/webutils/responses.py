from django.http import HttpResponse


class HttpResponseCodes():
    @classmethod
    def payload_too_large(cls) -> dict:
        """Return HttpResponse with status code 413."""
        return HttpResponse(status=413)
