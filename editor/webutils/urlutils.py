from django.contrib.sites.models import Site


class URLUtils:
    def get_current_domain():
        return Site.objects.get_current().domain
