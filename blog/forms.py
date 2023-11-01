from django import forms
from django.forms import ModelForm
from blog.models import UserMedia, Post, Comment
from django.contrib.auth.models import User


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('email', 'username', 'password')

class UserMediaForm(ModelForm):
    class Meta():
        model = UserMedia
        fields = ('profile_pic',)


class PostForm(ModelForm):    
    class Meta():
        model = Post
        fields = ('title', 'text',)

        

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)



