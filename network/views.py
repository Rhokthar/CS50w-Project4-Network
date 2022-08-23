import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import *

@login_required(login_url='login')
def index(request):
    # Check for User
    try:
        user = User.objects.get(id=request.user.id)
    except:
        messages.error(request, "User not found")
    
    # Check for Post
    try:
        posts = Post.objects.all().order_by("-creation_date")
    except:
        messages.error(request, "Post not found")
    
    # Return all Posts in Inverse Chrono-Order
    try:
        postsPaginator = Paginator(posts, 10)
        pageNumber = request.GET.get("page")
        postsPage = postsPaginator.get_page(pageNumber)

        return render(request, "network/index.html", {
            "page": postsPage,
            "user_liked_posts": user.liked_posts.all()
        })
    except:
        messages.error(request, "Something went wrong")
        return HttpResponseRedirect(reverse("index"))


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

@login_required(login_url='login')
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


# NEW POST VIEW STARTS
@login_required(login_url="login")
def new_post(request):
    # Vars
    postContent = request.POST["new-post-text"]
    
    # Check Passed Values
    if postContent != "":
        # Try Create Post
        try:
            user = User.objects.get(id=request.user.id)
            Post.objects.create(user=user, post_content=postContent)
            messages.success(request, "Post created successfully!")
        except:
            messages.error(request, "Something went wrong")

        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Can't submit a blank post!")
        return HttpResponseRedirect(reverse("index"))
# NEW POST VIEW ENDS


# PROFILE VIEW STARTS
@login_required(login_url="login")
def profile(request, profile_username):
    # Vars
    profileVisitedUser = User.objects.get(username=profile_username)
    visitingUser = User.objects.get(username=request.user.username)
    userPosts = Post.objects.filter(user=profileVisitedUser).order_by("-creation_date")
    followStatus = IsFollower(request, profileVisitedUser)
    
    # Check if Users Exists
    if (profileVisitedUser == None or visitingUser == None):
        messages.error(request, "Profile not found")
        return render(request, "network/profile.html")

    # Method -> Get -> Show Stuff
    if request.method == "GET":        
        return render(request, "network/profile.html", {
            "username": profile_username,
            "followers": profileVisitedUser.followers_list,
            "following": profileVisitedUser.following_list,
            "posts": userPosts,
            "follow_status": followStatus
        })
    
    # Method -> POST -> Follow/Unfollow Clicked
    else:
        # Not a Follower
        if not followStatus:
            profileVisitedUser.followers_list.add(visitingUser)
            visitingUser.following_list.add(profileVisitedUser)

            profileVisitedUser.save()
            visitingUser.save()
            messages.success(request, f"{profile_username} followed successfully!")
        # A Follower
        else:
            profileVisitedUser.followers_list.remove(visitingUser)
            visitingUser.following_list.remove(profileVisitedUser)
            
            profileVisitedUser.save()
            visitingUser.save()
            messages.success(request, f"{profile_username} unfollowed successfully!")
       
        return HttpResponseRedirect(reverse("profile", kwargs={"profile_username": profile_username}))
# PROFILE VIEW ENDS

# FOLLOWING-PAGE VIEW STARTS
@login_required(login_url="login")
def following_page(request):
    # Prendi gli utenti che followa chi va su questa pagina (request.user)
    usersFollowed = request.user.following_list.all()
    # Prendi i post degli utenti followati
    posts = Post.objects.filter(user__in=usersFollowed).order_by("-creation_date")

    return render(request, "network/following.html", {
        "posts": posts
    })
# FOLLOWING-PAGE VIEW ENDS


# EDIT-POST VIEW STARTS
@csrf_exempt
@login_required(login_url="login")
def edit_post(request, post_ID):
    # Check if Post Exists
    try:
        post = Post.objects.get(id=post_ID)
    except:
        messages.error(request, "Post not found")
        return HttpResponseRedirect(reverse("index"))
    
    # Get Post Json
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update Post Content
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post_content") is not None:
            post.post_content = data["post_content"]
        post.save()
        return HttpResponse(status=204)
# EDIT-POST VIEW ENDS


# LIKE-POST VIEW STARTS
@csrf_exempt
@login_required(login_url="login")
def like_post(request, post_ID):
    try:
        post = Post.objects.get(id=post_ID)
    except:
        messages.error(request, "Post not found")
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        # Get User
        try:
            likingUser = User.objects.get(id=request.user.id)
        except:
            messages.error(request, "User not found")
            return HttpResponseRedirect(reverse("index"))

        # Get All Post Liked by User
        likedPosts = likingUser.liked_posts.all()

        # If Post Already Liked
        if post in likedPosts and len(likedPosts) > 0:
            # Remove Like & Post Liked by User
            post.likes -= 1
            likingUser.liked_posts.remove(post)

        else:
            # Add Like & Post Liked by User
            post.likes += 1
            likingUser.liked_posts.add(post)
        
        # Save Updates
        post.save()
        likingUser.save()
        return HttpResponse(status=204)
# LIKE-POST VIEW ENDS