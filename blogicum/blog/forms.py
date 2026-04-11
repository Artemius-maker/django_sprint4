# Импортируем модель поздравления.
from django import forms
from .models import Post, Comment, User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date',
                  'location', 'category', 'is_published', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
