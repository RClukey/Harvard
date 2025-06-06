from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from EasyApps import views as uploader_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("university/<int:college>", views.uni, name="uni"),
    path("apply/<int:college_id>", views.apply, name="apply"),
    path("profile/edit/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("profile/<str:college>/<str:profile>", views.accept, name="accept"),
]