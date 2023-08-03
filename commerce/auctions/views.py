from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import auction_listings, User, bids, comments, connect_two, closed_listings
from django.db.models import Max

CATEGORY_LIST= [
    ('Fashion', 'Fashion'),
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
    ('Education', 'Education')
]
global global_username
class NewEntryForm(forms.Form):
    Title = forms.CharField(label = 'Title', widget = forms.TextInput(attrs={'style': 'width: 300px','class': 'form-control'}))
    URL = forms.CharField(label = 'URL', widget = forms.TextInput(attrs={'style': 'width: 500px', 'class': 'form-control'}), required = False)
    Description = forms.CharField(label = 'Description', widget = forms.TextInput(attrs={'style': 'width: 500px', 'class': 'form-control'}))
    Price = forms.CharField(label = 'Price:', widget = forms.TextInput(attrs={'style': 'width: 500px', 'class': 'form-control'}))
    Date = forms.DateField(label = 'Date', widget = forms.DateInput(attrs={'placeholder':'mm/dd/yyyy','style': 'width: 500px', 'class': 'form-control'}))
    Category = forms.CharField(label = "Category", widget = forms.Select(choices = CATEGORY_LIST))

class BidForm(forms.Form):
    Bid = forms.CharField(label ='', widget = forms.TextInput(attrs={'placeholder':'Bid (in USD)','style':'width:300px','class':'form-control'}))

class add_comment_form(forms.Form):
    Comment = forms.CharField(label = "Add a New Comment:", widget = forms.Textarea(attrs = {'style':'width:300px','class':'form-control'}))

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
        global username
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
            data = connect_two(username = username)
            data.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    return render(request,"auctions/new_listing.html",{
        "form": NewEntryForm(),
    })

def add_listing(request,username):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['Title']
            url = form.cleaned_data['URL']
            description = form.cleaned_data['Description']
            price = form.cleaned_data['Price']
            category = form.cleaned_data['Category']
            date = form.cleaned_data['Date']
            name = username
            saving = auction_listings(name = name, title = title, url = url, description = description,price = price,category=category,date=date)
            saving.save()
            save_price = bids(title = title, bids_made = price)
            save_price.save()
            return render(request,"auctions/index.html",{
                "data": auction_listings.objects.all(),
            })
        else:
            return render(request,"auctions/login.html")
    else:
            return render(request,"auctions/login.html")
    
def index(request):
    return render(request, "auctions/index.html",{
        "data": auction_listings.objects.all()
    })

def view_listing(request, title):
    past_username = auction_listings.objects.get(title = title)
    past_username = past_username.name
    usernames = request.user
    usernames = usernames.username
    check_text = bool (past_username == usernames)
    if check_text == True:
        return render(request,"auctions/view_list.html",{
            "data": auction_listings.objects.filter(title = title),
            "form": BidForm(),
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title),
            "check_text": check_text
        })
    elif check_text == False:
        return render(request,"auctions/view_list.html",{
            "data": auction_listings.objects.filter(title = title),
            "form": BidForm(),
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title)
        })    
    else:
        return HttpResponse("Error: 404")

def new_bid(request, title, username):
    past_username = auction_listings.objects.get(title = title)
    past_username = past_username.name
    check_text = bool (past_username == username)
    if check_text == True:
        form = BidForm(request.POST)
        if form.is_valid():
                new_value = int(form.cleaned_data['Bid'])
                max = bids.objects.filter(title = title).aggregate(Max('id'))
                max = max['id__max']
                get_bid_info = bids.objects.get(title = title, id = max)
                last_bid = int(get_bid_info.bids_made)
                if new_value > last_bid:
                    saving = bids(title = title, username = username, bids_made = new_value)
                    saving.save()
                    t = auction_listings.objects.get(title = title)
                    t.price = new_value
                    t.save()
                    return render(request, "auctions/view_list.html",{
                        "bid_made": "The bid has been made",
                        "data": auction_listings.objects.filter(title = title),
                        "form": BidForm(),
                        "form_comment": add_comment_form(),
                        "comments": comments.objects.filter(title = title),
                        "check_text": check_text
                    })
                else:
                    return render(request, "auctions/view_list.html",{
                        "error": "The bid could be made because the value you entered is lower than the previous bid or starting bid.",
                        "data": auction_listings.objects.filter(title = title),
                        "form": BidForm(),
                        "comments": comments.objects.filter(title = title),
                        "form-comment": add_comment_form(),
                        "check_text": check_text
                    })
    elif check_text == False:
        form = BidForm(request.POST)
        if form.is_valid():
                new_value = int(form.cleaned_data['Bid'])
                max = bids.objects.filter(title = title).aggregate(Max('id'))
                max = max['id__max']
                get_bid_info = bids.objects.get(title = title, id = max)
                last_bid = int(get_bid_info.bids_made)
                if new_value > last_bid:
                    saving = bids(title = title, username = username, bids_made = new_value)
                    saving.save()
                    t = auction_listings.objects.get(title = title)
                    t.price = new_value
                    t.save()
                    return render(request, "auctions/view_list.html",{
                        "bid_made": "The bid has been made",
                        "data": auction_listings.objects.filter(title = title),
                        "form": BidForm(),
                        "form_comment": add_comment_form(),
                        "comments": comments.objects.filter(title = title)
                    })
                else:
                    return render(request, "auctions/view_list.html",{
                        "error": "The bid could be made because the value you entered is lower than the previous bid or starting bid.",
                        "data": auction_listings.objects.filter(title = title),
                        "form": BidForm(),
                        "comments": comments.objects.filter(title = title),
                        "form-comment": add_comment_form()
                    })
    else:
        return HttpResponse("Error: 404")
values = [0]
def add_watchlist(request, username, title, id):
    past_username = auction_listings.objects.get(title = title)
    past_username = past_username.name
    check_text = bool (past_username == username)
    if check_text == True:
        listing = auction_listings.objects.get(title = title)
        usernames = connect_two.objects.get(username = username)
        usernames.user_linking.add(listing)
        return render(request,"auctions/view_list.html",{
            "message": "Item added to Watchlist.",
            "data": auction_listings.objects.filter(title = title),
            "check": 'Remove from Watchlist',
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title),
            "check_text": check_text
        })
    elif check_text == False:
        listing = auction_listings.objects.get(title = title)
        usernames = connect_two.objects.get(username = username)
        usernames.user_linking.add(listing)
        return render(request,"auctions/view_list.html",{
            "message": "Item added to Watchlist.",
            "data": auction_listings.objects.filter(title = title),
            "check": 'Remove from Watchlist',
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title)
        })
    else:
        return HttpResponse("Error: 404")

def remove_watchlist(request, username, title, id):
    past_username = auction_listings.objects.get(title = title)
    past_username = past_username.name
    check_text = bool (past_username == username)
    if check_text == True:
        listing = auction_listings.objects.get(title = title)
        usernames = connect_two.objects.get(username = username)
        usernames.user_linking.remove(listing)
        return render(request,"auctions/view_list.html",{
            "note": "Item deleted from Watchlist.",
            "data": auction_listings.objects.filter(title = title),
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title),
            "check_text": check_text
        })
    elif check_text == False:
        listing = auction_listings.objects.get(title = title)
        usernames = connect_two.objects.get(username = username)
        usernames.user_linking.remove(listing)
        return render(request,"auctions/view_list.html",{
            "note": "Item deleted from Watchlist.",
            "data": auction_listings.objects.filter(title = title),
            "form_comment": add_comment_form(),
            "comments": comments.objects.filter(title = title)
        })
    else:
        return HttpResponse("Error: 404")

def watch_list(request,username):
    usernames = connect_two.objects.get(username = username)
    data = usernames.user_linking.all()
    return render(request, "auctions/watchlist.html",{
        "data": data,
        "check": "Remove from Watchlist"
    })

def categories(request):
    data = auction_listings.objects.all()
    return render(request, "auctions/categories.html", {
        "data": data
    })

def fashion(request):
    fashion = auction_listings.objects.filter(category = "Fashion")
    return render(request, "auctions/viewing_category.html",{
        "data": fashion,
        "name": 'Fashion'
    })

def toys(request):
    toys = auction_listings.objects.filter(category = "Toys")
    return render(request, "auctions/viewing_category.html",{
        "data": toys,
        "name": 'Toys'
    })

def electronics(request):
    electronics = auction_listings.objects.filter(category = 'Electronics')
    return render(request, "auctions/viewing_category.html",{
        "data": electronics,
        "name": 'Electronics'
    })

def home(request):
    home = auction_listings.objects.filter(category = "Home")
    return render(request, "auctions/viewing_category.html",{
        'data': home,
        "name": 'Home'
    })

def education(request):
    education = auction_listings.objects.filter(category = "Education")
    return render(request, "auctions/viewing_category.html",{
        'data': education,
        "name": 'Education'
    })

def add_comment(request, username, title):
    past_username = auction_listings.objects.get(title = title)
    past_username = past_username.name
    check_text = bool (past_username == username)
    if check_text == True:
        if request.method == "POST":
            form = add_comment_form(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['Comment']
                saving = comments(comment = comment, username = username, title = title)
                saving.save()
                return render(request, "auctions/view_list.html",{
                    "data": auction_listings.objects.filter(title = title),
                    "form": BidForm(),
                    "form_comment": add_comment_form(),
                    "comment_success": "Comment added successfully",
                    "comments": comments.objects.filter(title = title),
                    "check_text": check_text
                })
    elif check_text == False:
        if request.method == "POST":
            form = add_comment_form(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['Comment']
                saving = comments(comment = comment, username = username, title = title)
                saving.save()
                return render(request, "auctions/view_list.html",{
                    "data": auction_listings.objects.filter(title = title),
                    "form": BidForm(),
                    "form_comment": add_comment_form(),
                    "comment_success": "Comment added successfully",
                    "comments": comments.objects.filter(title = title),
                })
    else:
        return HttpResponse("Error: 404")
    
def close_auction(request, title):
    auction_data = auction_listings.objects.get(title = title)
    name = auction_data.name
    url = auction_data.url
    description = auction_data.description
    price = auction_data.price
    date = auction_data.date
    category = auction_data.category
    usernames = bids.objects.get(title = title, bids_made = price)
    username = usernames.username
    current_user = request.user
    current_user = current_user.username
    name = auction_listings.objects.get(title = title)
    name = name.name
    saving = closed_listings(name = name, title = title, url = url, description = description, price = price, date = date, category = category, username = username)
    saving.save()
    removing = auction_listings.objects.get(title = title)
    removing.delete()
    return render(request, "auctions/view_list.html",{
        "update": "Auction listing successfully closed"
    })

def closed_listing(request):
    current_user = request.user
    current_user = current_user.username
    return render(request, "auctions/closed_auc_list.html",{
        "data": closed_listings.objects.filter(username = current_user),
    })