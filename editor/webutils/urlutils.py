from django.contrib.sites.models import Site


class URLUtils:
    def get_current_domain():
        return Site.objects.get_current().domain

    def get_filename_from_url(url: str):
        """Return last word from the url.

        If url will be as follows:
        'https://example.com/some/path/to/file.jpg'
        Function result will be:
        'file.jpg'
        """
        return url.split('/')[-1]
