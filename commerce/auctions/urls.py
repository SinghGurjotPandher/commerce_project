from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.new_listing, name = "create_listing"),
    path("add_listing/<str:username>", views.add_listing, name = "add_listing"),
    path("view_listing/<str:title>", views.view_listing, name = "view_listing"),
    path("watch_list/<str:username>", views.watch_list, name = "watch_list"),
    path("add_watchlist/<str:username>/<str:title>/<int:id>", views.add_watchlist, name = "add_watchlist"),
    path("remove_watchlist/<str:username>/<str:title>/<int:id>", views.remove_watchlist, name = "remove_watchlist"),
    path("categories", views.categories, name = "categories"),
    path("fashion", views.fashion, name = "fashion"),
    path("toys", views.toys, name = "toys"),
    path("electronics", views.electronics, name = "electronics"),
    path("home", views.home, name = "home"),
    path("education", views.education, name = "education"),
    path("new_bid/<str:title>/<str:username>", views.new_bid, name = "new_bid"),
    path("add_comment/<str:username>/<str:title>", views.add_comment, name = "add_comment"),
    path("close_auction/<str:title>", views.close_auction, name = "close_auction"),
    path("closed_listing", views.closed_listing, name = "closed_listing")
]
