from django.contrib.auth.models import AbstractUser
from django.db import models

# Users Table
class User(AbstractUser):
    followers_list = models.ManyToManyField("User", default=None, blank=True, related_name="followers")
    following_list = models.ManyToManyField("User", default=None, blank=True, related_name="following")
    liked_posts = models.ManyToManyField("Post", default=None, blank=True, related_name="liked_posts")

    def show_followers(self):
        return ", ".join([follower.username for follower in self.followers_list.all()])
    
    def show_following(self):
        return ", ".join([following.username for following in self.following_list.all()])

    def show_liked_posts(self):
        return ", ".join([str(liked_post.id) for liked_post in self.liked_posts.all()])


# Posts Table
class Post(models.Model):
    # ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post_content = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    # TODO
    # comment
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post_content": self.post_content,
            "creation_date": self.creation_date,
            "likes": self.likes
        }