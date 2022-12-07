from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Food, User

food_data = Food.objects.all()

def index(request):
    # if not request.user.is_authenticated:
    #     redirect to login page
    user_data = request.session.get("user_data", "guest")
    if "cart_data" not in request.session:
        request.session["cart_data"] = []
    return render(request, "ordering/index.html", {"data": food_data, "user": user_data})

def cart(request):
    return render(request, "ordering/cart.html", {"data": request.session["cart_data"]})

def add(request):
    if request.method == "POST":
        request.session["cart_data"] += [request.POST["food_name"]] #test
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect(reverse("ordering:cart"))

def login(request):
    if request.method == "POST":
        try: 
            user_data = User.objects.get(username = request.POST["username"], password = request.POST["password"])
            request.session["user_data"] = user_data.username
            messages.success(request, "login สำเร็จ")
        except:
            messages.error(request, "login ไม่สำเร็จ")
        return HttpResponseRedirect("/")
    return render(request, "ordering/login.html")

def logout(request):
    request.session.pop("user_data")
    return HttpResponseRedirect("/")

