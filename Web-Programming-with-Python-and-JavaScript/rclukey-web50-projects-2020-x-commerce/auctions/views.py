from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bidding, Comment

Categories = ["Weapons", "Clothing", "Food", "Riches", "Instruments", "Misc"]

def index(request):
    active_listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "active": active_listings,
        "message": "Active Listings"
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

@login_required
def create_listing(request):
    if request.method == "POST":
        name = request.POST["listing_title"]
        url = request.POST["image_url"]
        desc = request.POST["description"]
        cat = request.POST["category"]
        lister = request.user

        bids = request.POST["starting_bid"]

        b = Bidding(bid=float(bids), bidded_by=lister)
        b.save()

        l = Listing(listing_name=name, image_url=url, description=desc, price=b, listed_by=lister, category=cat)
        l.save()

        return HttpResponseRedirect(reverse(index))
        
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": Categories
        })

@login_required
def watchlist(request):
    watchListings = request.user.watchlist_listing.all()
    return render(request, "auctions/index.html", {
        "active": watchListings,
        "message": f"Watchlist For {request.user}"
    })

def categories(request):
    if request.method == "POST":
        cat = request.POST["categ"]
        listings = Listing.objects.filter(category=cat)

        return render(request, "auctions/index.html", {
            "active": listings,
            "message": f"Category: {cat}"
        })

    else:
        return render(request, "auctions/categories.html", {
            "categories": Categories
        })

def category(request, categ):
    listings = Listing.objects.filter(category=categ)

    return render(request, "auctions/index.html", {
        "active": listings,
        "message": f"Category: {categ}"
    })

def lis(request, num):
    specific_listing = Listing.objects.get(id=num)
    in_watchlist = request.user  in specific_listing.watchlist.all()
    comments = Comment.objects.filter(listing_name=specific_listing)
    winner = specific_listing.price.bidded_by

    return render(request, "auctions/listing.html", {
        "listing": specific_listing,
        "in_watchlist": in_watchlist,
        "error": "",
        "user": request.user,
        "comments": comments,
        "winner": winner
    })

def bid(request, num):
    specific_listing = Listing.objects.get(id=num)

    bids = float(request.POST["new_bid"])

    if bids > float(specific_listing.price.bid):
         Bid = Bidding(bid=bids, bidded_by=request.user)
         Bid.save()

         specific_listing.price = Bid
         specific_listing.save()

         return HttpResponseRedirect(reverse("lis",args=(num, )))
    else:
        in_watchlist = request.user  in specific_listing.watchlist.all()

        return render(request, "auctions/listing.html", {
            "listing": specific_listing,
            "in_watchlist": in_watchlist,
            "user": request.user,
            "error": "You must bid higher than the current price.",
            "comments": Comment.objects.filter(listing_name=specific_listing)
        })

def comment(request, num):
    comments = request.POST["comment"]
    commentor = request.user
    comment_on = Listing.objects.get(id=num)

    c = Comment(listing_name = comment_on, commented_by = commentor, comment = comments)
    c.save()

    return HttpResponseRedirect(reverse("lis",args=(num, )))

def add(request, num):
    specific_listing = Listing.objects.get(id=num)
    specific_listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("lis",args=(num, )))

def remove(request, num):
    specific_listing = Listing.objects.get(id=num)
    specific_listing.watchlist.remove(request.user)
    
    return HttpResponseRedirect(reverse("lis",args=(num, )))

def close_auction(request, num):
    closed = Listing.objects.get(id=num)
    closed.is_active = False
    closed.save()

    winner = closed.price.bidded_by
    in_watchlist = request.user  in closed.watchlist.all()

    return render(request, "auctions/listing.html", {
        "listing": closed,
        "in_watchlist": in_watchlist,
        "user": request.user,
        "error": "",
        "comments": Comment.objects.filter(listing_name=closed),
        "winner": winner
    })
