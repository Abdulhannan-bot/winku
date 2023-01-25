from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django import forms


class Account(models.Model):
  user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
  email = models.EmailField(max_length = 224, null = True)
  full_name = models.CharField(max_length = 100, null = True)
  created_at = models.DateTimeField(auto_now_add = True, null = True)
  profile_pic = models.ImageField(default="user_29hrBtO.png", null = True, blank = True)
  background_pic = models.ImageField(default="cover-photo_hVs4cgX_G9aAZgR.png", null = True, blank = True)

  def __str__(self):
    return str(self.user)

class Post(models.Model):
  description = models.TextField(null = True, blank = True)
  # text = models.TextField(null = True, blank = True)
  File = models.FileField(upload_to='media', null = True, blank = True)
  user_id = models.ForeignKey(Account, null = True, blank=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add = True, null = True)


  def __str__(self):
    return str(self.created_at)
  
class Comment(models.Model):
  text = models.TextField(null = True)
  post_id = models.ForeignKey(Post, null = True, blank = True, on_delete=models.SET_NULL)
  user_id = models.ForeignKey(Account, null = True, blank = True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add = True, null = True)


  def __str__(self):
    return str(self.text[:10])+"....."

class Like(models.Model):
  user_id = models.ForeignKey(Account, null = True, blank = False, on_delete=models.SET_NULL, related_name="post_by")
  post_id = models.ForeignKey(Post, null = True, blank = False, on_delete=models.SET_NULL)
  liked_by = models.ForeignKey(Account, null = True, blank = False, on_delete=models.SET_NULL, )

  def __str__(self):
    return str(self.liked_by) + " likes a post by " + str(self.user_id)

class Follower(models.Model):
  follower_id = models.ForeignKey(Account, related_name = 'follower', null = True, on_delete=models.SET_NULL)
  followee_id = models.ForeignKey(Account, related_name = 'followee', null = True, on_delete=models.SET_NULL)

  def __str__(self):
    return str(self.follower_id)+" follows "+str(self.followee_id)

class Activity(models.Model):
  log = models.CharField(max_length = 200, null = True)
  created_at = models.DateTimeField(auto_now_add = True, null = True)

@receiver(post_save, sender = User)
def user_generator(sender, created, instance, **kwargs):
  if created:
    Account.objects.create(
      user = instance,
      email = instance.email,
      full_name = instance.first_name+" "+instance.last_name
    )

