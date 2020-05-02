from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from editor.blog import views


urlpatterns = [
    path('', views.home_view, name="blog-home"),
    path('contact', views.contact_view, name="blog-contact"),
    path('about', views.about_view, name="blog-about"),
    path('post', views.post_view, name="blog-post"),
    path('404', views.page_not_found_view, name="blog-404"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
