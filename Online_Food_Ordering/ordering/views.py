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
    if request.session.get("user_id") == None:
        messages.error(request, 'Please, login.')
        return HttpResponseRedirect("/")
    if request.method == "POST":
        # check if that item already exists in the cart
        added = False
        cart_data = request.session["cart_data"]
        for item in cart_data:
            if item[0] == request.POST["food_id"]:
                item[2] += int(request.POST["food_quantity"])
                request.session["cart_data"] = cart_data
                added = True
                break
        if not added:
            request.session["cart_data"] += [(request.POST["food_id"], request.POST["food_name"], int(request.POST['food_quantity']), float(request.POST['food_price']))]
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect("/")

# cart
def cart(request):
    if request.session.get("user_id") == None:
        messages.error(request, 'Please, login.')
        return HttpResponseRedirect("/")
    if request.session["cart_data"] == []:
        messages.error(request, "The cart is empty")
        return HttpResponseRedirect("/")
    mockup = [(item[0], item[1], f"{item[2]}x{item[3]}", f"{item[2]*item[3]}฿") for item in request.session["cart_data"]]
    total = sum(int(x[2])*float(x[3]) for x in request.session["cart_data"])
    user_name = request.session.get("user_name", "guest")
    return render(request, "ordering/cart.html", {"data": mockup, "total": total, "user":user_name})

def clear_cart(request):
    request.session["cart_data"] = []
    return HttpResponseRedirect(reverse("ordering:cart"))

def delete_item(request):
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
    total = sum(x[2]*x[3] for x in request.session["cart_data"])
    user = User.objects.get(id=request.session["user_id"])
    entry = Order_User(order_id = d.now().strftime("%y%m%d%H%M%S"), user=user, date=d.now().strftime("%d-%m-%y"), total=total)
    entry.save()
    # Order table
    for item in request.session["cart_data"]:
        food = Food.objects.get(id=item[0])
        quantity = item[2]
        order = Order(order=entry, food=food, quantity=quantity)
        order.save()
    request.session["cart_data"] = []
    messages.success(request,"Confirmed!")
    return HttpResponseRedirect("/")

# orders page
def orders(request):
    if request.session.get("user_id") == None:
        messages.error(request, 'Please, login.')
        return HttpResponseRedirect("/")
    user = User.objects.get(id=request.session["user_id"])
    order_list = Order_User.objects.filter(user=user)
    # use Order_User objects to search in order table
    order_data = []
    for order in order_list:
        item_list = Order.objects.filter(order=order) # get specific rows that match the order_id
        mockup = [(i.food.name, f"{i.quantity}x{i.food.price}", f"{int(i.quantity)*float(i.food.price)}฿") for i in item_list]
        order_data += [(order.order_id, order.date, order.total, mockup)]
    user_name = request.session.get("user_name", "guest")
    return render(request, "ordering/orders.html", {"data": order_data, "user":user_name})

def delete_order(request):
    if request.method == "POST":
        Order_User.objects.filter(order_id=request.POST["order_id"]).delete()
        messages.success(request, "The order has been deleted.")
    return HttpResponseRedirect(reverse("ordering:orders"))

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

def register(request):
    if request.method == "POST":
        try:
            user_data = User.objects.get(username = request.POST["reguser"])
        except:
            user_data = None
        if user_data:
            messages.error(request,"ซ้ำ")
        else:
            if request.POST['reguser'] == 'guest':
                messages.error(request,"ซ้ำ")
            else:
                reg = User.objects.create(username = request.POST['reguser'],password = request.POST['regpassword'])
                messages.success(request,"สมัครสำเร็จ")
        return HttpResponseRedirect("/")
    return render(request, "ordering/register.html")

# profile
def profile(request):
    if request.session.get("user_id") == None:
        messages.error(request, 'Please, login.')
        return HttpResponseRedirect("/")
    if request.method == "POST":
        if request.POST["new-password"] == request.POST["confirm-password"]:
            user = User.objects.get(id=request.session["user_id"])
            user.password = request.POST["new-password"]
            user.save()
            messages.success(request, "You have changed your password.")
        else:
            messages.error(request, "Something went wrong.")
        return HttpResponseRedirect("/")
    user_name = request.session.get("user_name", "guest")
    return render(request, "ordering/profile.html", {"user":user_name})