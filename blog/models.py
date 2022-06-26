from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Topic(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name

    # def get_absolute_url(self):
    #     return reverse('topic_detail', kwargs={'pk': self.pk})


class Post(models.Model):
    Author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Topic_post = models.ManyToManyField(Topic)
    Post_name = models.CharField(max_length=100)
    Overview = models.CharField(max_length=60, null=True)
    Content = RichTextField(blank=True, null=True)
    Thumbnail = models.ImageField(blank=True, null=True,default='post-1.png')
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    # # class Meta:
    #     ordering = ['-Created', '-Updated']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post_update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Post_name

    @property
    def get_comments(self):
        return self.comments.all()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[0:50]

