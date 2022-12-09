from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from datetime import datetime as d

food_data = Food.objects.all()
# index
def index(request):
    user_name = request.session.get("user_name", "guest")
    return render(request, "ordering/index.html", {"data": food_data, "user": user_name})

def add(request):
    # if request.session.get("user_id") == None:
    #     messages.error(request, 'Please, login.')
    #     return HttpResponseRedirect("/")
    if request.method == "POST":
        request.session["cart_data"] += [(request.POST["food_id"], request.POST["food_name"], request.POST['food_quantity'], request.POST['food_price'])]
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect("/")

# cart
def cart(request):
    user_name = request.session.get("user_name", "guest")
    if request.session["cart_data"] == []:
        messages.error(request, "The cart is empty")
        return HttpResponseRedirect("/")
    mockup = [(item[0], item[1], f"{item[2]}x{item[3]}", f"{int(item[2])*float(item[3])}฿") for item in request.session["cart_data"]]
    return render(request, "ordering/cart.html", {"data": mockup, "user": user_name})

def clear_cart(request):
    request.session["cart_data"] = []
    return HttpResponseRedirect(reverse("ordering:cart"))

def delete(request):
    if request.method == "POST":
        cart_data = request.session["cart_data"]
        for index, item in enumerate(cart_data):
            if item[0] == request.POST["food_id"]:
                cart_data.pop(index)
                request.session["cart_data"] = cart_data
                break
    return HttpResponseRedirect(reverse("ordering:cart"))

def confirm_order(request):
    # Order_User table
    entry = Order_User(order_id = d.now().strftime("%y%m%d%H%M%S"), user=User.objects.get(id=request.session["user_id"]))
    entry.save()
    # Order table
    for item in request.session["cart_data"]:
        food = Food.objects.get(id=item[0])
        quantity = item[2]
        order = Order(order=entry, date=d.now().strftime("%d-%m-%y"), food=food, quantity=quantity)
        order.save()
    request.session["cart_data"] = []
    return HttpResponseRedirect("/")

# login
def login(request):
    if request.method == "POST":
        try: 
            user_data = User.objects.get(username = request.POST["username"], password = request.POST["password"])
            request.session["user_name"] = user_data.username
            request.session["user_id"] = user_data.id
            request.session["cart_data"] = []
            messages.success(request, "login สำเร็จ")
        except:
            messages.error(request, "login ไม่สำเร็จ")
        return HttpResponseRedirect("/")
    return render(request, "ordering/login.html")

def logout(request):
    request.session.pop("user_name")
    request.session.pop("user_id")
    request.session.pop("cart_data")
    return HttpResponseRedirect("/")

