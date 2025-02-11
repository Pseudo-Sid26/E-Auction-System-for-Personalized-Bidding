# Import JsonResponse to handle JSON responses
import requests  # Make sure to import the requests module
from django.http import JsonResponse
from .models import watchlist  # Assuming your watchlist model is in the same app
from django.shortcuts import render, redirect, get_object_or_404
from gradio import Interface
import threading
from django.shortcuts import render
from django.http import HttpResponse
from gradio_client import Client
import gradio as gr
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, auctionlist, bids, comments, watchlist, winner
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import User, auctionlist, bids, comments, watchlist, winner


# Modified index view
def index(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Get personalized recommendations
        recommendations = get_recommendations(request.user)
        return render(request, "auctions/index.html", {
            "recommendations": recommendations,
            "personalized": True,  # Flag to display recommendations
        })
    else:
        # Show regular active listings for non-logged in users
        return render(request, "auctions/index.html", {
            "a1": auctionlist.objects.filter(active_bool=True),
            "personalized": False,  # Flag to show general listings
        })


# Recommendation system function
# def get_recommendations(user):
#     # Step 1: Fetch user activity from the database
#     user_bids = bids.objects.filter(user=user.username)
#     user_watchlist = watchlist.objects.filter(user=user.username)

#     # Step 2: Build a preference vector based on their interactions
#     user_interests = {}

#     for bid in user_bids:
#         auction = auctionlist.objects.get(pk=bid.listingid)
#         category = auction.category
#         user_interests[category] = user_interests.get(category, 0) + 1

#     for watch in user_watchlist:
#         category = watch.watch_list.category
#         user_interests[category] = user_interests.get(category, 0) + 1

#     # Step 3: Compare with all auction items to find similarity
#     all_auctions = auctionlist.objects.filter(active_bool=True)
#     recommendations = []

#     for auction in all_auctions:
#         interest_vector = [user_interests.get(auction.category, 0)]
#         auction_vector = [1]
#         similarity = cosine_similarity([interest_vector], [auction_vector])
#         recommendations.append((auction, similarity[0][0]))  # Store the similarity score directly

#     # Step 4: Sort by similarity and return top 70% recommendations
#     recommendations.sort(key=lambda x: x[1], reverse=True)

#     # Calculate 70% of the total recommendations
#     total_recommendations = len(recommendations)
#     top_n = max(int(total_recommendations * 0.7), 1)  # Ensure at least 1 recommendation is returned

    # return [rec[0] for rec in recommendations[:top_n]]  # Return top 70% recommendations

#! updated recommendation system code
def get_recommendations(user):
    # Step 1: Fetch user activity from the database
    user_bids = bids.objects.filter(user=user.username)
    user_watchlist = watchlist.objects.filter(user=user.username)

    # Step 2: Build a preference vector based on their interactions
    user_interests = {}

    for bid in user_bids:
        try:
            auction = auctionlist.objects.get(pk=bid.listingid)
            category = auction.category
            user_interests[category] = user_interests.get(category, 0) + 1
        except auctionlist.DoesNotExist:
            # Skip this bid if the auction doesn't exist
            continue

    for watch in user_watchlist:
        try:
            auction = auctionlist.objects.get(pk=watch.watch_list.id)
            category = auction.category
            user_interests[category] = user_interests.get(category, 0) + 1
        except auctionlist.DoesNotExist:
            continue

    # Step 3: Compare with all auction items to find similarity
    all_auctions = auctionlist.objects.filter(active_bool=True)
    recommendations = []

    for auction in all_auctions:
        interest_vector = [user_interests.get(auction.category, 0)]
        auction_vector = [1]
        similarity = cosine_similarity([interest_vector], [auction_vector])
        # Store the similarity score directly
        recommendations.append((auction, similarity[0][0]))

    # Step 4: Sort by similarity and return top 70% recommendations
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Calculate 70% of the total recommendations
    total_recommendations = len(recommendations)
    # Ensure at least 1 recommendation is returned
    top_n = max(int(total_recommendations * 0.7), 1)

    # Return top 70% recommendations
    return [rec[0] for rec in recommendations[:top_n]]


# Import necessary libraries


# change in def 1
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to personalized recommendations page after login
            return HttpResponseRedirect(reverse("personalized_dashboard"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# change in def 2


@login_required(login_url='login')
def personalized_dashboard(request):
    # Call the recommendation system for the logged-in user
    recommendations = get_recommendations(request.user)

    # Render the existing index.html template but with recommendations data
    return render(request, "auctions/index.html", {
        "a1": recommendations,
    })


def recommended_auctions(request):
    if request.user.is_authenticated:
        recommendations = get_recommendations(request.user)
    else:
        recommendations = auctionlist.objects.filter(
            active_bool=True).order_by('-id')[:5]  # Default recommendations
    return render(request, "auctions/recommended.html", {
        "recommendations": recommendations
    })


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


@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        m = auctionlist()
        m.user = request.user.username
        m.title = request.POST["create_title"]
        m.desc = request.POST["create_desc"]
        m.starting_bid = request.POST["create_initial_bid"]
        m.image_url = request.POST["img_url"]
        m.category = request.POST["category"]
        # m = auctionlist(title = title, desc=desc, starting_bid = starting_bid, image_url = image_url, category = category)
        m.save()
        return redirect("index")
    return render(request, "auctions/create.html")


def listingpage(request, bidid):
    biddesc = auctionlist.objects.get(pk=bidid, active_bool=True)
    bids_present = bids.objects.filter(listingid=bidid)

    return render(request, "auctions/listingpage.html", {
        "list": biddesc,
        "comments": comments.objects.filter(listingid=bidid),
        "present_bid": minbid(biddesc.starting_bid, bids_present),
    })


@login_required(login_url='login')
def watchlistpage(request, username):

    # present_w = watchlist.objects.get(user = "username")
    list_ = watchlist.objects.filter(user=username)
    return render(request, "auctions/watchlist.html", {
        "user_watchlist": list_,
    })


@login_required(login_url='login')
def addwatchlist(request):
    nid = request.GET["listid"]

    # below line of code will select a table of watchlist that has my name, then
    # when we loop in this watchlist, there r two fields present, to browse watch_list
    # watch_list.id == auctionlist.id, similar for all

    list_ = watchlist.objects.filter(user=request.user.username)

    # when you below line, you shld convert id to int inorder to compare or else == wont work

    for items in list_:
        if int(items.watch_list.id) == int(nid):
            return watchlistpage(request, request.user.username)

    newwatchlist = watchlist(watch_list=auctionlist.objects.get(
        pk=nid), user=request.user.username)
    newwatchlist.save()
    # this message remains untill u reload
    messages.success(request, "Item added to watchlist")

    return listingpage(request, nid)


@login_required(login_url='login')
def deletewatchlist(request):
    if request.method == "POST":
        rm_id = request.POST.get("listid")
        list_ = get_object_or_404(watchlist, pk=rm_id, user=request.user)

        # Display success message
        messages.success(
            request, f"{list_.watch_list.title} is deleted from your watchlist.")
        list_.delete()

        return redirect("index")
    else:
        return redirect("index")  # Redirect in case of non-POST request

# this function returns minimum bid required to place a user's bid


def minbid(min_bid, present_bid):
    for bids_list in present_bid:
        if min_bid < int(bids_list.bid):
            min_bid = int(bids_list.bid)
    return min_bid


@login_required(login_url='login')
def bid(request):
    bid_amnt = request.GET["bid_amnt"]
    list_id = request.GET["list_d"]
    bids_present = bids.objects.filter(listingid=list_id)
    startingbid = auctionlist.objects.get(pk=list_id)
    min_req_bid = startingbid.starting_bid
    min_req_bid = minbid(min_req_bid, bids_present)

    if int(bid_amnt) > int(min_req_bid):
        mybid = bids(user=request.user.username,
                     listingid=list_id, bid=bid_amnt)
        mybid.save()
        messages.success(request, "Bid Placed")
        return redirect("index")

    messages.warning(request, f"Sorry, {
                     bid_amnt} is less. It should be more than {min_req_bid}$.")
    return listingpage(request, list_id)


# shows comments made by different user and allows to add comments
@login_required(login_url='login')
def allcomments(request):
    comment = request.GET["comment"]
    username = request.user.username
    list_id = request.GET["listid"]
    new_comment = comments(user=username, comment=comment, listingid=list_id)
    new_comment.save()
    return listingpage(request, list_id)


# shows message abt winner when bid is closed
def win_ner(request):
    bid_id = request.GET["listid"]
    bids_present = bids.objects.filter(listingid=bid_id)
    biddesc = auctionlist.objects.get(pk=bid_id, active_bool=True)
    max_bid = minbid(biddesc.starting_bid, bids_present)
    try:
        # checks if anyone other than list_owner win the bid
        winner_object = bids.objects.get(bid=max_bid, listingid=bid_id)
        winner_obj = auctionlist.objects.get(id=bid_id)
        win = winner(bid_win_list=winner_obj, user=winner_object.user)
        winners_name = winner_object.user

    except:
        # if no-one placed a bid, and if bid is closed by list_owner, owner wins the bid
        winner_obj = auctionlist.objects.get(starting_bid=max_bid, id=bid_id)
        win = winner(bid_win_list=winner_obj, user=winner_obj.user)
        winners_name = winner_obj.user

    # Check Django Documentary for Updating attributes based on existing fields.
    biddesc.active_bool = False
    biddesc.save()

    # saving winner details
    win.save()
    messages.success(request, f"{winners_name} won {win.bid_win_list.title}.")
    return redirect("index")

# checks winner


def winnings(request):
    try:
        your_win = winner.objects.filter(user=request.user.username)
    except:
        your_win = None

    return render(request, "auctions/winnings.html", {
        "user_winlist": your_win,
    })

# shows lists that are present in a specific category


def cat(request, category_name):
    category = auctionlist.objects.filter(category=category_name)
    return render(request, "auctions/index.html", {
        "a1": category,
    })

# shows all categories in which object is listed


def cat_list(request):

    # unlike filter that takes a values of object_name in model, to
    # display objectname use .values('name of section from your object')
    # and when you add distinct() along with it
    # it shows only unique names, omits duplicates

    category_present = auctionlist.objects.values('category').distinct()
    return render(request, "auctions/category.html", {
        "cat_list": category_present,
    })


# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": "fdbdf#####################################"}

# Function to call the Hugging Face API


def query_huggingface(payload, max_length=512):
    payload["options"] = {"max_length": max_length}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to filter or preprocess the input based on e-commerce context


def preprocess_ecommerce_question(question):
    # E-commerce specific keywords
    keywords = ['product', 'price', 'order', 'return', 'shipping', 'category', 'cart',
                'payment', 'refund', 'discount', 'Nike', 'Adidas', 'Samsung', 'Apple',
                'Sony', 'earphones', 'headphones', 'smartphone', 'laptop', 'tablet',
                'charger', 'case', 'shoes', 'clothing']

    # If the question contains any of the e-commerce related keywords, proceed
    if any(keyword.lower() in question.lower() for keyword in keywords):
        return question
    else:
        return "Can you ask something related to our e-commerce services?"

# Chatbot view for Django


def chatbot_view(request):
    if request.method == 'POST':
        # Get the question from the POST request
        question = request.POST.get('question')

        # Preprocess the question to focus on e-commerce topics
        processed_question = preprocess_ecommerce_question(question)

        # Prepare the payload for the Hugging Face model
        payload = {"inputs": processed_question}

        # Call the Hugging Face model and get the response
        output = query_huggingface(payload, max_length=512)

        # Extract the generated text
        generated_text = output[0]['generated_text']

        # Return the generated text as a JSON response
        return JsonResponse({'response': generated_text})

    return render(request, 'auctions/chatbot.html')
