from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_list, watch_list
from django import forms


def index(request):
    al = auction_list.objects.all()
    return render(request, "auctions/index.html", {
        "all_item": al
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class NewListForm(forms.Form):
    name = forms.CharField(label="Item name")
    description = forms.CharField(label="Description", widget=forms.Textarea() )
    money = forms.IntegerField(label="Starting Bid")
    img = forms.CharField(label="Image Link")

def create_listing(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            name = form.name
            description = form.description
            bid = form.money
            img_link = form.img
            new_auction = auction_list(item=name, price=bid, image=img_link, desc=description)
            return HttpResponseRedirect(reverse("index/"))
        else :
            return render(request, 'auctions/add_list.html', {
                "form": form
            })
    return render(request, 'auctions/add_list.html', {
        "form": NewListForm()
    })
            
def show_watch_list(request):
    TODO