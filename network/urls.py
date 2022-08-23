from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("new-post", views.new_post, name="new-post"),
    path("profile/<str:profile_username>", views.profile, name="profile"),
    path("following-page", views.following_page, name="following_page")
]
