from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import HttpResponse

from editor.blog_admin.models import Post as PostModel


def home_view(request):
    return render(request, 'home-masonry.html')


def page_not_found_view(request):
    return render(request, 'page-404.html')


def contact_view(request):
    return render(request, 'page-contact.html')


def about_view(request):
    return render(request, 'page-about.html')


def test_view(request):
    if request.method == 'GET':
        # import pdb; pdb.set_trace()
        post = PostModel.objects.latest('id')
        hashtag = post.hashtags.all().values().first()['text']
        # hashtags = [tag['text'] for tag in hashtags]
        return render(
            request, 'test.html', {'post': post, 'hashtag': hashtag}
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
