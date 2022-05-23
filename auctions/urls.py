from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.show_watch_list, name="watchlist"),
    path("add_watch_list/<str:target>", views.add_watch_list, name="add_watch_list"),
    path("listing/<str:item_name>/", views.show_listing, name="show_listing"),
    path("make_a_bid/<str:item_name>", views.make_a_bid, name="make_a_bid")
]
