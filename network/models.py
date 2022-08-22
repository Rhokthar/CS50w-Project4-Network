from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    # ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post_content = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    # TODO
    # comment
    likes = models.IntegerField(default=0)

    def post_view(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post_content": self.post_content,
            "creation_date": self.creation_date,
            "likes": self.likes
        }