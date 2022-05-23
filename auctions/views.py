from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_list, watch_list, bid
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def index(request):
    al = auction_list.objects.all()
    if request.user.is_authenticated and watch_list.objects.all().filter(user=request.user).exists():
        print("hhhhhhh")
        return render(request, "auctions/index.html", {
        "all_item": al,
        "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all()
    })
        
    return render(request, "auctions/index.html", {
        "all_item": al,
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

            auto_add = watch_list(user=user)
            auto_add.save()
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

# @login_required
def create_listing(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            name = form.name
            description = form.description
            bbid = form.money
            img_link = form.img
            new_auction = auction_list(item=name, price=bbid, image=img_link, desc=description)
            return HttpResponseRedirect(reverse("index/"))
        else :
            return render(request, 'auctions/add_list.html', {
                "form": form,
                "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all()
            })
    return render(request, 'auctions/add_list.html', {
        "form": NewListForm(),
        "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all()
    })

# # @login_required            
# def show_watch_list(request):
#     cur_watch_list = watch_list.objects.all().get(user=request.user)
#     print(cur_watch_list.all_list)
#     return render(request, 'auctions/watch_list.html', {
#         "items": cur_watch_list.all_list.all()
#     })

@login_required
def show_watch_list(request):
    all_items = auction_list.objects.all()
    print(all_items)
    # cur_watch_list = []
    cur_watch_list = watch_list.objects.all().filter(user=request.user)
    # print('ffff')
    # print(cur_watch_list.get(user=request.user).all_list.all().count)
    # print('ffff')
    # if cur_watch_list.get(user=request.user).all_list.all().count:
    #     return render(request, 'auctions/index.html', {
    #         "error": "No items in watch list",
    #     })
    return render(request, 'auctions/watch_list.html', {
        "all_items": all_items,
        "watch_list_items": cur_watch_list.get(user=request.user).all_list.all()
    })

def add_watch_list(request, target):
    print(request.path)
    cur_item = auction_list.objects.get(item=target)
    cur_watch_list = watch_list.objects.get(user=request.user)
    if watch_list.objects.all().filter(user=request.user).exists() and cur_item in cur_watch_list.all_list.all():
        cur_watch_list.all_list.remove(cur_item)
        cur_watch_list.save()
    else:
        cur_watch_list.all_list.add(cur_item)
        cur_watch_list.save()
    return HttpResponseRedirect(f"/listing/{target}")

class newBid(forms.Form):
    my_bid = forms.IntegerField(label="My Bid")


def show_listing(request, item_name):
    now_item = auction_list.objects.get(item=item_name)
    return render(request, 'auctions/listing.html', {
        "item_object": now_item, 
        "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all(),
        "bid_form": newBid()
    })

def make_a_bid(request, item_name):
    print(request.method)
    form = newBid(request.POST)
    if form.is_valid():
        bid_price = form.cleaned_data["my_bid"]
        cur_price = auction_list.objects.all().get(item=item_name).current_bid
        # print(type(cur_price))
        if bid_price > cur_price:
            new_bid = bid(user=request.user, my_bid=bid_price, my_target=auction_list.objects.all().get(item=item_name))
            new_bid.save()
            change_target = auction_list.objects.get(item=item_name)
            change_target.current_bid = bid_price
            change_target.save()
            return HttpResponseRedirect(f"/listing/{item_name}")
            # return render(request, 'auctions/listing.html', {
            #     "item_object": auction_list.objects.get(item=item_name),
            #     "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all(),
            #     "bid_form": newBid(),
            #     "msg": "Successfully Bid!"
            # })
        else :
            return render(request, 'auctions/listing.html', {
                "item_object": auction_list.objects.get(item=item_name),
                "watch_list_items": watch_list.objects.all().filter(user=request.user).get(user=request.user).all_list.all(),
                "bid_form": form,
                "msg": "Your bid must be higher than current price!"
            })
