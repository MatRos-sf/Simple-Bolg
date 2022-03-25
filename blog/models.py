from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('funny', 'Funny'),
        ('history', 'History'),
        ('information', 'Information'),
        ('interesting', 'interesting'),
        ('nature', 'Nature'),
        ('news', 'News'),
        ('sport', 'Sport')
    )
    category = models.CharField(max_length=12,
                                choices=CATEGORY_CHOICES,
                                default='interesting')
    title = models.CharField(max_length=100)
    body = models.TextField()
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.category,
                             self.id])
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return "Comment added by {} from the post {}".format(self.name, self.post)

