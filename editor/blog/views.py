from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.conf import settings

from editor.blog_admin.models import Post as PostModel


def home_view(request):
    return render(request, 'home-masonry.html')


def page_not_found_view(request):
    return render(request, 'page-404.html')


def contact_view(request):
    return render(request, 'page-contact.html')


def about_view(request):
    return render(request, 'page-about.html')


class BlogListView(ListView):
    def __init__(self):
        self.paginate_by = settings.POSTS_PER_PAGE
        self.context_object_name = 'post_list'
        self.queryset = PostModel.get_published_posts_by_date()
        self.template_name = 'post_tiles.html'
        self.allow_empty = False


class PostDetailView(DetailView):
    model = PostModel
    template_name = 'post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieving linked tags from the db
        tags = self.object.hashtags.values()
        # Parsing tag objects and getting text values
        context['hashtags'] = [tag['text'] for tag in tags]

        return context


class PostLatestView(PostDetailView):

    def get_object(self, queryset=None):
        post = PostModel.objects.latest('modified_date')
        return post
