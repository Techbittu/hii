from django import forms
from django.contrib.auth.models import User
from .models import Profile , post

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','bio']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title','author','content','img','category','slug']