from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.


class Signup(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email