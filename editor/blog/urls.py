from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from editor.blog import views


app_name = 'blog'
urlpatterns = [
    path('', views.home_view, name="home"),
    path('contact/', views.contact_view, name="contact"),
    path('about/', views.about_view, name="about"),
    path('post/', views.post_view, name="post"),
    path('404/', views.page_not_found_view, name="404"),
]
