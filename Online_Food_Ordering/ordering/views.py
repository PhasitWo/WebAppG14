from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Food

food_data = Food.objects.all()

def index(request):
    # if not request.user.is_authenticated:
    #     redirect to login page
    if "cart_data" not in request.session:
        request.session["cart_data"] = []
    return render(request, "ordering/index.html", {"data": food_data})

def cart(request):
    return render(request, "ordering/cart.html", {"data": request.session["cart_data"]})

def add(request):
    if request.method == "POST":
        request.session["cart_data"] += [request.POST["food_name"]] #test
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect(reverse("ordering:cart"))