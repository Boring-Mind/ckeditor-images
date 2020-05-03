from django.db import models


class Hashtags(models.Model):
    text = models.CharField(max_length=30)


POST_STATUSES = [
    ('DR', 'Draft'),
    ('ST', 'Stash'),
    ('PB', 'Public'),
]


class Post(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=300)
    hashtags = models.ManyToManyField(Hashtags)
    content = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    # ToDo: add image load via the file input
    # or via the url input (if image is hosted somewhere else)
    preview_img_url = models.CharField(max_length=250)
    post_status = models.CharField(
        max_length=2, choices=POST_STATUSES, default='DR'
    )
    
    class Meta:
        ordering = ['post_date']

    def __str__(self):
        return f'{self.post_date}: \"{self.title}\"'
