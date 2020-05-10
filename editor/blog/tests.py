from django.test import TestCase


class IntegrationTests(TestCase):
    """Holds all integration tests for blog app."""

    def test_uses_home_view(self):
        response = self.client.get('/blog/')
        self.assertTemplateUsed(response, 'home-masonry.html')

    def test_uses_404_view(self):
        response = self.client.get('/blog/404')
        self.assertTemplateUsed(response, 'page-404.html')

    def test_uses_contact_view(self):
        response = self.client.get('/blog/contact')
        self.assertTemplateUsed(response, 'page-contact.html')

    def test_uses_about_view(self):
        response = self.client.get('/blog/about')
        self.assertTemplateUsed(response, 'page-about.html')

    def test_uses_post_view(self):
        response = self.client.get('/blog/post')
        self.assertTemplateUsed(response, 'post-detail.html')
