from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Food, User

food_data = Food.objects.all()

def index(request):
    user_data = request.session.get("user_data", "guest")
    if "cart_data" not in request.session:
        request.session["cart_data"] = []
    return render(request, "ordering/index.html", {"data": food_data, "user": user_data})

def cart(request):
    user_data = request.session.get("user_data", "guest")
    mockup = [(item[0], item[1], f"{item[2]}x{item[3]}", f"{int(item[2])*float(item[3])}฿") for item in request.session["cart_data"]]
    return render(request, "ordering/cart.html", {"data": mockup, "user": user_data})

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

def add(request):
    if request.method == "POST":
        request.session["cart_data"] += [(request.POST["food_id"], request.POST["food_name"], request.POST['food_quantity'], request.POST['food_price'])]
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect("/")

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

