from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categ>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:num>", views.lis, name="lis"),
    path("listing/<int:num>/add", views.add, name="add"),
    path("listing/<int:num>/remove", views.remove, name="remove"),
    path("listing/<int:num>/close", views.close_auction, name="close_auction"),
    path("listing/<int:num>/bid", views.bid, name="bid"),
    path("listing/<int:num>/comment", views.comment, name="comment"),
]
