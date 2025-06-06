from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("id").reverse()

    paginator = Paginator(posts, 10)
    page_index = request.GET.get("page")
    page_posts = paginator.get_page(page_index)

    all_liked_posts = Like.objects.filter()
    liked_posts = []

    try:
        for post in all_liked_posts:
            if post.user_liked.id == request.user.id:
                liked_posts.append(post.post_liked.id)
    except:
        liked_posts = []

    return render(request, "network/index.html", {
        "posts": page_posts,
        "message": "All Posts",
        "liked_posts": liked_posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        post = request.POST["new_post"]

        p = Post(poster=user, message=post)
        p.save()
        return HttpResponseRedirect(reverse("index"))

def following(request):
    current_user = User.objects.get(id=request.user.id)
    user_follows = Follow.objects.filter(user_following=current_user)
    posts = Post.objects.all().order_by('id').reverse()

    follower_posts = []

    for post in posts:
        for person in user_follows:
            if person.user_followed == post.poster:
                follower_posts.append(post)
    
    paginator = Paginator(follower_posts, 10)
    page_index = request.GET.get("page")
    page_posts = paginator.get_page(page_index)

    all_liked_posts = Like.objects.filter()
    liked_posts = []

    try:
        for post in all_liked_posts:
            if post.user_liked.id == request.user.id:
                liked_posts.append(post.post_liked.id)
    except:
        liked_posts = []

    return render(request, "network/index.html", {
        "posts": page_posts,
        "message": "Following",
        "post_username": current_user.username,
        "liked_posts": liked_posts,
    })

def profile(request, user):
    id = User.objects.get(username=user)

    posts = id.posts.all()
    posts = posts.order_by("id").reverse()

    paginator = Paginator(posts, 10)
    page_index = request.GET.get("page")
    page_posts = paginator.get_page(page_index)

    followers = Follow.objects.filter(user_followed=id)
    following = Follow.objects.filter(user_following=id)

    try:
        check_following = followers.filter(user_following=User.objects.get(id=request.user.id))
        is_following = len(check_following) != 0
    except:
        is_following = False

    all_liked_posts = Like.objects.filter()
    liked_posts = []

    try:
        for post in all_liked_posts:
            if post.user_liked.id == request.user.id:
                liked_posts.append(post.post_liked.id)
    except:
        liked_posts = []

    return render(request, "network/index.html", {
        "posts": page_posts,
        "message": f"{user}'s Posts",
        "num_followers": followers.count(),
        "num_following": following.count(),
        "post_username": user,
        "is_following": is_following,
        "liked_posts": liked_posts,
    })

def follow(request, user):
    id = User.objects.get(username=user)
    current_user = User.objects.get(id=request.user.id)

    f = Follow(user_following=current_user, user_followed=id)
    f.save()

    return HttpResponseRedirect(reverse("profile",args=(user, )))

def unfollow(request, user):
    id = User.objects.get(username=user)
    current_user= User.objects.get(id=request.user.id)

    f = Follow.objects.get(user_following=current_user, user_followed=id)
    f.delete()

    return HttpResponseRedirect(reverse("profile",args=(user, )))

def edit(request, post):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(id=post)
        edit_post.message = data["message"]
        edit_post.save()
        return JsonResponse({"message":"Change Successful", "data": data["message"]})

def like(request, post):
    current_user = User.objects.get(id=request.user.id)
    message = Post.objects.get(id=post)
    
    l = Like(user_liked = current_user, post_liked = message)
    l.save()

    return JsonResponse({"message":"Like Added"})

def unlike(request, post):
    current_user = User.objects.get(id=request.user.id)
    message = Post.objects.get(id=post)
    
    l = Like.objects.get(user_liked = current_user, post_liked = message)
    l.delete()

    return JsonResponse({"message":"Like Removed"})