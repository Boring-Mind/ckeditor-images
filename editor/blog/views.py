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


class PostWithTag:
    def __init__(self, post, tag):
        self.post = post
        self.tag = tag


class BlogListView(ListView):
    def __init__(self):
        self.paginate_by = settings.POSTS_PER_PAGE
        self.context_object_name = 'post_list'
        self.queryset = PostModel.get_published_posts_by_date()
        self.template_name = 'post_tiles.html'
        self.allow_empty = False

    # ToDo: refactor
    def get_context_data(self):
        context = super().get_context_data()
        posts = context['post_list']

        tags = [post.get_first_tag() for post in posts]

        posts = posts.values()

        post_list = []
        for i, post in enumerate(posts):
            post_list.append(PostWithTag(post, tags[i]))
        context['post_list'] = post_list

        return context


# Deprecated
# def blog_page_view(request):
#     if request.method == 'GET':
#         # import pdb; pdb.set_trace()
#         page = int(request.GET.get('page', 0))
#         posts_per_page = settings.POSTS_PER_PAGE
#         posts = PostModel.objects.order_by('modified_date')[page * posts_per_page:(page+1) * posts_per_page]
#         hashtags = [
#             post.get_first_tag() for post in posts
#         ]

#         post_list = []
#         for i, post in enumerate(posts):
#             post_list.append(PostWithTag(post, hashtags[i]))

#         return render(request, 'test_cycle.html', {'post_list': post_list})
#     else:
#         return HttpResponse('', status=404)


# def test_view(request):
#     if request.method == 'GET':
#         # import pdb; pdb.set_trace()
#         post = PostModel.objects.latest('id')
#         hashtag = post.hashtags.all().values().first()['text']
#         # hashtags = [tag['text'] for tag in hashtags]
#         return render(
#             request, 'test.html', {'post': post, 'hashtag': hashtag}
#         )
#     else:
#         return HttpResponse('', status=404)


def tile_test_view(request):
    if request.method == 'GET':
        posts = PostModel.objects.order_by('-id')
        hashtag = posts[0].hashtags.all().values().first()['text']
        # hashtags = [tag['text'] for tag in hashtags]
        return render(
            request, 'test_cycle.html', {'posts': posts, 'hashtag': hashtag}
        )
    else:
        return HttpResponse('', status=404)


class PostDetailView(DetailView):
    model = PostModel
    template_name = 'post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieving linked tags from the db
        tags = self.object.hashtags.all().values()
        # Parsing tag objects and getting text values
        context['hashtags'] = [tag['text'] for tag in tags]

        return context


class PostLatestView(PostDetailView):

    def get_object(self, queryset=None):
        post = PostModel.objects.latest('id')
        return post
