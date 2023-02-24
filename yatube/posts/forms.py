from django import forms
from django.forms import Textarea

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': ('Текст поста'),
            'group': ('Группа'),
        }
        help_texts = {
            'text': ('Напишите красивый пост'),
            'group': ('Выберите группу'),
        }
        widgets = {
            'text': Textarea,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
