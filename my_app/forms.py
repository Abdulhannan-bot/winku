from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from foundation_filefield_widget.widgets import FoundationFileInput, FoundationImageInput
from django.core.files import File
from PIL import Image

from .models import *

class SignUpForm(UserCreationForm):
  username = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  first_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  last_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, widget = forms.EmailInput(attrs = {'class': "form-control"}))
  password1 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))
  password2 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AccountForm(ModelForm):
  full_name = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  class Meta:
    model = Account
    fields = ['full_name', 'email']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ['created_at']

class SearchForm(ModelForm):
  username = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
    
class PostForm(ModelForm):
  x = forms.FloatField(widget=forms.HiddenInput(), required=False)
  y = forms.FloatField(widget=forms.HiddenInput(), required=False)
  width = forms.FloatField(widget=forms.HiddenInput(), required=False)
  height = forms.FloatField(widget=forms.HiddenInput(), required=False)
  description = forms.CharField(widget = forms.TextInput(attrs = {'class': "form-control", 'placeholder': 'Write something ...'}), required=False),

  class Meta:
    model = Post
    fields = ['File', 'description', 'x', 'y', 'width', 'height', ]
    # widgets = {
    #   'File': FoundationFileInput(attrs = {'class': "form-control"}, renderer=None),
    # }
  
  def save(self, *args, **kwargs):
    post = super(PostForm, self).save()
    if post.File:
      
      x = self.cleaned_data.get('x')
      y = self.cleaned_data.get('y')
      w = self.cleaned_data.get('width')
      h = self.cleaned_data.get('height')

      if(x and y and w and h):

        image = Image.open(post.File)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(post.File.path)

    return post

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ['created_at']

  

class CoverPhotoForm(ModelForm):
  x = forms.FloatField(widget=forms.HiddenInput(), required=False)
  y = forms.FloatField(widget=forms.HiddenInput(), required=False)
  width = forms.FloatField(widget=forms.HiddenInput(), required=False)
  height = forms.FloatField(widget=forms.HiddenInput(), required=False)
  class Meta:
    model = Account
    fields = ['background_pic']

  def save(self, *args, **kwargs):
    cover = super(CoverPhotoForm, self).save()
    if cover.background_pic:
      
      x = self.cleaned_data.get('x')
      y = self.cleaned_data.get('y')
      w = self.cleaned_data.get('width')
      h = self.cleaned_data.get('height')

      if(x and y and w and h):

        image = Image.open(cover.background_pic)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((195, 80), Image.ANTIALIAS)
        resized_image.save(cover.background_pic.path)

    return cover


class ProfilePhotoForm(ModelForm):
  x1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
  y1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
  width1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
  height1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
  class Meta:
    model = Account
    fields = ['profile_pic']

  def save(self, *args, **kwargs):
    profile = super(ProfilePhotoForm, self).save()
    if profile.profile_pic:
      
      x1 = self.cleaned_data.get('x1')
      y1 = self.cleaned_data.get('y1')
      w1 = self.cleaned_data.get('width1')
      h1 = self.cleaned_data.get('height1')

      if(x1 and y1 and w1 and h1):

        image = Image.open(profile.profile_pic)
        cropped_image = image.crop((x1, y1, w1+x1, h1+y1))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.profile_pic.path)

    return profile