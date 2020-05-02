from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from editor.blog import views


urlpatterns = [
    path('', views.home_view, name="blog-home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
