from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Comment


class PostForm(forms.ModelForm):
    class Meta:
            model = Post
            fields = ['Post_name','Overview','Topic_post', 'Content','Thumbnail']
            # fields = ['Overview', 'Post_name']


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'comment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ['content',]