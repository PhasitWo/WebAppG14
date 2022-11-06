from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Food

# test cart (change to session later)
cart = [] 

data = Food.objects.all()

def index(request):
    return render(request, "ordering/index.html", {"data": data})

def add(request):
    if request.method == "POST":
        # some process here
        #....
        messages.success(request, 'Item has been added to the cart.')
    return HttpResponseRedirect(reverse("ordering:index"))