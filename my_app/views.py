from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from json import dumps
import pytesseract
# from django.utils import simplejson
# Create your views here.

try:
  from PIL import Image as Im
except:
  import Image

from .forms import *
from .models import *
from .decorators import *

@unauthenticated_user
def register_view(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      try:
        form.save()
        messages.info(request,'Account created successfully')
        return redirect("login")
      except ValueError:
        messages.error(request,'Account with that username already exists. Pick another username')
  context = {
    "form": form,
  }
  return render(request, "register.html", context)

@unauthenticated_user
def login_view(request):
  if(request.method == "POST"):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    user1 = User.objects.filter(username = username).filter(password = password)
    print(user1)
    if(user is not None):
      login(request, user)
      return redirect('home')
    else:
      print("not authenticated")
  return render(request, "login.html")

@login_required(login_url = 'login')
@csrf_exempt
def home(request):
  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]
  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)
  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""
  
  # PostImageFormset = inlineformset_factory(Account, Post, form = PostForm, extra=1)
  # account = Account.objects.get(user = request.user)
  # formset = PostImageFormset(queryset = Post.objects.none(), instance = account)
  # initial_dict = {
  #       "user_id" : account,
  #   }
  post_form = PostForm()


  context = {}
  
  # print(accounts.count())
  # count = accounts.count()
  # print(f'count - {count}')
  posts = Post.objects.none()
  following = Follower.objects.none()
  likes = Like.objects.none()
  likes_list = []
  # if count:
  count = Post.objects.filter(user_id__in = account_list).count()
  posts = reversed(Post.objects.filter(user_id__in = account_list).order_by('created_at'))
  following = Follower.objects.filter(follower_id = account)
  follower = Follower.objects.filter(followee_id = account)
  likes = Like.objects.filter(liked_by = request.user.account)
  my_likes = Like.objects.filter(user_id = request.user.account)
  

  for i in likes:
    likes_list.append(i.post_id)
  comments_form = CommentForm()
  print(likes_list)
  data = "text:text"


  context = {
    "accounts": accounts,
    "count": count,
    "following": following,
    "follower": follower,
    "likes": likes,
    "likes_list": likes_list,
    "posts": posts,
    "account_search": account_search,
    "value": value,
    "post_form": post_form,
    "comments_form": comments_form,
    "my_likes": my_likes,
  }
  if request.method == "POST":
    print(request.FILES)
    if(request.FILES.get('File')):
      response_data = {}
      upload = request.FILES.get('File')
      content = pytesseract.image_to_string(Im.open(upload))
      response_data['content'] = content
      li = response_data['content'].split('\n')
      diction = {
        "li": li
      }
      dataJSON = json.dumps(diction)
      print(li)
      context["data"] = dataJSON

    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)
      context['account_search'] = account_search
      context['value'] = value

  return render(request, "home.html", context = context)




@login_required(login_url = 'login')
def your_profile(request):
  cover_initial = {
    "background_pic": ""
  }
  cover_form = CoverPhotoForm(instance = request.user.account, initial = cover_initial)

  profile_initial = {
    "profile_pic": ""
  }
  profile_form = ProfilePhotoForm(instance = request.user.account, initial = profile_initial)

  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]


  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)


  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""

  if request.method == "POST":
    cover_form = CoverPhotoForm(request.POST, request.FILES, instance = request.user.account)
    if cover_form.is_valid():
      cover_form.save()

    profile_form = ProfilePhotoForm(request.POST, request.FILES, instance = request.user.account)
    if profile_form.is_valid():
      profile_form.save()

    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)

  count = Post.objects.filter(user_id = account).count()
  posts = reversed(Post.objects.filter(user_id = account).order_by('created_at'))
  following = Follower.objects.filter(follower_id = account)
  follower = Follower.objects.filter(followee_id = account)
  like = Like.objects.filter(user_id = request.user.account).count()
  context = {
    "count": count,
    "following": following,
    "follower": follower,
    "like": like,
    # "likes_list": likes_list,
    "posts": posts,
    "account_search": account_search,
    "value": value,
    "cover_form": cover_form,
    "profile_form": profile_form,
    "account": account,
    "friends": False,
  }
  return render(request, "your-profile.html", context = context)

@login_required(login_url = 'login')
def add_post(request):
  print(request.POST)
  PostImageFormset = inlineformset_factory(Account, Post, form = PostForm, extra=1)
  account = Account.objects.get(user = request.user)
  formset = PostImageFormset(queryset = Post.objects.none(), instance = account)
  # initial_dict = {
  #       "user_id" : account,
  #   }
  post_form = PostForm()
  
  if request.method == 'POST':
    post_form = PostForm(request.POST, request.FILES)
    if post_form.is_valid():
      obj = post_form.save(commit = False)
      obj.user_id = account
      print(post_form.cleaned_data)
      obj.save()
      # formset.save(commit=False)
    else:
      print("not_saved")
  return redirect('home')

@login_required(login_url = 'login')
def add_comment(request, id):
  post = Post.objects.get(id = id)
  form = CommentForm()
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      obj = form.save(commit = False)
      obj.post_id = post
      obj.user_id = request.user.account
      obj.save()
      
  context = {
    "form": form,
  }
  return redirect('home')

@login_required(login_url = 'login')
def add_followee(request, id):
  print("followee entered")
  follower = Account.objects.get(user = request.user)
  followee = Account.objects.get(id = id)
  Follower.objects.create(follower_id = follower, followee_id = followee)

  return redirect('home')

@login_required(login_url = 'login')
def remove_followee(request, id):
  account = Account.objects.get(user = request.user)
  following = Follower.objects.filter(follower_id = account).filter(followee_id = Account.objects.get(id = id))
  following.delete()
  context = {
    "following":following,
  }
  return redirect('home')

@login_required(login_url = 'login')
def likes(request, id):
  post = Post.objects.get(id = id)
  user = User.objects.get(username = post.user_id)
  account = Account.objects.get(user = user)
  like_by = Account.objects.get(user = request.user)
  Like.objects.create(user_id = account, post_id = post, liked_by = like_by)
  context = {
    "liked": True,
  }
  return redirect('home')

@login_required(login_url = 'login')
def unlike(request, id):
  post = Post.objects.get(id = id)
  user = User.objects.get(username = post.user_id)
  account = Account.objects.get(user = user)
  like = Like.objects.filter(post_id = post).filter(user_id = account).filter(liked_by = request.user.account)
  like.delete()
  context = {
    "liked": False,
  }
  return redirect('home')

@login_required(login_url = 'login')
def delete_post(request, id):
  post = Post.objects.get(id = id)
  post.delete()
  return redirect('home')

@login_required(login_url = 'login')
def friends(request):
  cover_initial = {
    "background_pic": ""
  }
  cover_form = CoverPhotoForm(instance = request.user.account, initial = cover_initial)

  profile_initial = {
    "profile_pic": ""
  }
  profile_form = ProfilePhotoForm(instance = request.user.account, initial = profile_initial)

  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]
  
  my_follow = Follower.objects.filter(follower_id = request.user.account)
  friend_list = []
  for i in my_follow:
    if(Follower.objects.filter(follower_id = i.followee_id).filter(followee_id = i.follower_id).exists()):
      friend_list.append(i.followee_id)
  print(friend_list)
  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)


  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""

  if request.method == "POST":
    cover_form = CoverPhotoForm(request.POST, request.FILES, instance = request.user.account)
    if cover_form.is_valid():
      cover_form.save()

    profile_form = ProfilePhotoForm(request.POST, request.FILES, instance = request.user.account)
    if profile_form.is_valid():
      profile_form.save()

    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)

  following = Follower.objects.filter(follower_id = account)
  follower = Follower.objects.filter(followee_id = account)
  like = Like.objects.filter(user_id = request.user.account).count()
  context = {
    "following": following,
    "follower": follower,
    "like": like,
    "account_search": account_search,
    "value": value,
    "cover_form": cover_form,
    "profile_form": profile_form,
    "account": account,
    "friends": False,
    "friends": friend_list,
    "friends_len": len(friend_list),
  }
  return render(request, "friends.html", context = context)

@login_required(login_url = 'login')
def about(request):
  cover_initial = {
    "background_pic": ""
  }
  cover_form = CoverPhotoForm(instance = request.user.account, initial = cover_initial)

  profile_initial = {
    "profile_pic": ""
  }
  profile_form = ProfilePhotoForm(instance = request.user.account, initial = profile_initial)

  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]
  
  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)


  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""

  account_form = AccountForm(instance = request.user.account)

  if request.method == "POST":
    cover_form = CoverPhotoForm(request.POST, request.FILES, instance = request.user.account)
    if cover_form.is_valid():
      cover_form.save()

    profile_form = ProfilePhotoForm(request.POST, request.FILES, instance = request.user.account)
    if profile_form.is_valid():
      profile_form.save()
    
    account_form = AccountForm(request.POST, instance = request.user.account)
    if account_form.is_valid():
      account_form.save()

    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)

  

  following = Follower.objects.filter(follower_id = account)
  follower = Follower.objects.filter(followee_id = account)
  like = Like.objects.filter(user_id = request.user.account).count()
  context = {
    "following": following,
    "follower": follower,
    "like": like,
    "account_search": account_search,
    "value": value,
    "cover_form": cover_form,
    "profile_form": profile_form,
    "account": account,
    "account_form": account_form,
  }
  
  return render(request, "about.html", context = context)

@login_required(login_url = 'login')
def follower_profile(request, id):
  account = Account.objects.get(id = id)
  posts = Post.objects.filter(user_id = account)
  followers = Follower.objects.filter(followee_id = account).count()
  following = Follower.objects.filter(follower_id = account).count()
  like = Like.objects.filter(user_id = account).count()
  follow = False
  post_show = False
  posts = Post.objects.filter(user_id = account)
  post_count = 0
  for post in posts:
    post_count += post.like_set.count()
  print(post_count)



  follows = Follower.objects.all()
  exclude_list = [request.user]
  my_account = Account.objects.get(user = request.user)
  account_list = [my_account]


  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)


  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""

  my_following = Follower.objects.filter(follower_id = my_account)
  my_follower = Follower.objects.filter(followee_id = my_account)
  

  if Follower.objects.filter(follower_id = request.user.account).filter(followee_id = account).exists():
    follow = True
    post_show = True

  if request.method == "POST":
    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)

  context = {
    "my_account": my_account,
    "account": account,
    "posts": posts,
    "followers": followers,
    "following": following,
    "follow": follow,
    "posts": posts,
    "post_show": post_show,
    "like": like,
    "account_search": account_search,
    "value": value,
    "my_following": my_following,
    "my_follower": my_follower,

  }
  return render(request, "follower-profile.html", context = context)


@login_required(login_url = 'login')
def logout_trigger(request):
  logout(request)
  return redirect('login')