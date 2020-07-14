from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.utils.translation import gettext_lazy as _
# from validator import Validator


class Hashtags(models.Model):
    text = models.CharField(max_length=35, unique=True)


POST_STATUSES = [
    ('DR', 'Draft'),
    ('ST', 'Stash'),
    ('PB', 'Public'),
]


# class UsernameValidatorAllowSpaces(UnicodeUsernameValidator):
#     regex = r'^[\w\' _-]+\Z'
#     message = _(
#         'Enter a valid username. This value may contain only letters, '
#         'numbers, spaces and -/_/\' characters.'
#     )


# class UsernameValidatorAllowSpaces(Validator):
#     username = 'required|regex:^[\w\' _-]+\Z'

#     message = {
#         'username': {
#             'required': _('username is required'),
#             'regex': _(
#                 'Enter a valid username. This value may contain only letters, '
#                 'numbers, spaces and -/_/\' characters.'
#             )
#         }
#     }


# class UserModel(User):
#     username_validator = UsernameValidatorAllowSpaces

#     class Meta:
#         proxy = True


class Post(models.Model):
    # ToDo: Reduce length to 50 chars
    title = models.CharField(max_length=80)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    description = models.CharField(max_length=300)
    hashtags = models.ManyToManyField(Hashtags)
    content = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    # ToDo: add image load via the file input
    # or via the url input (if image is hosted somewhere else)
    preview_img_url = models.CharField(max_length=300)
    post_status = models.CharField(
        max_length=2, choices=POST_STATUSES, default='DR'
    )
    
    class Meta:
        ordering = ['post_date']

    def __str__(self):
        return (
            f'{self.post_date.strftime("%d.%m.%Y %H:%M")} - \"{self.title}\"'
        )

    # ToDo: add tests
    def get_first_tag(self):
        tag = self.hashtags.all().values().first()
        if tag:
            return tag['text']
        return ''

    def get_published_posts_by_date():
        queryset = Post.objects.filter(post_status='DR')
        queryset = queryset.order_by('-modified_date')
        if len(queryset) == 0:
            raise Http404('No Post object matches the given query.')
        return queryset
