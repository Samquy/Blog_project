from django.contrib import admin
from .models import Author,Topic,Post,Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Topic)
admin.site.register(Comment)