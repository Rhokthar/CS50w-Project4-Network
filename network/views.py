from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import *

@login_required(login_url='login')
def index(request):
    return render(request, "network/index.html")


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
    if postContent != None:
        # Try Create Post
        user = User.objects.get(id=request.user.id)
        Post.objects.create(user=user, post_content=postContent)
        messages.success(request, "Post created successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Can't submit a blank post!")
        return HttpResponseRedirect(reverse("index"))
# NEW POST VIEW ENDS


# ALL POSTS VIEW STARTS
@login_required(login_url="login")
def all_posts(request):
    # Return all Posts in Inverse Chrono-Order
    posts = Post.objects.all().order_by("-creation_date")
    return JsonResponse([post.post_view() for post in posts], safe=False)
# ALL POSTS VIEW ENDS
