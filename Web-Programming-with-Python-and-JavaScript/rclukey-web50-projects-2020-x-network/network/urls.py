
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post, name="new_posting"),
    path("following", views.following, name="following"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("profile/<str:user>/unfollow", views.unfollow, name="unfollow"),
    path("profile/<str:user>/follow", views.follow, name="follow"),
    path("edit/<int:post>", views.edit, name="edit"),
    path("like/<int:post>", views.like, name="like"),
    path("unlike/<int:post>", views.unlike, name="unlike")
]
