from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watch_list", views.show_watch_list, name="watch_list"),
    path("listings", views.show_list, name="listings"),
    path("add_watch_list/<str:target>", views.add_watch_list, name="add_watch_list")
]
