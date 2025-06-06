from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    message = models.TextField(blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Posted by {self.poster} on {self.timestamp}. Post: {self.message}"

class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"{self.user_following} is following {self.user_followed}"

class Like(models.Model):
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_user")
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user_liked} liked {self.post_liked}"