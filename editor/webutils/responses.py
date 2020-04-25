from django.http import HttpResponse


class HttpResponseCodes:
    """Holds shortcuts for different http responses."""
    
    @classmethod
    def payload_too_large(cls) -> dict:
        """Return HttpResponse with status code 413."""
        return HttpResponse(status=413)
