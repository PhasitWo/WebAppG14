from django.shortcuts import render
from django.http import HttpResponse
from .models import Food
# Create your views here.
def index(request):
    return render(request, "ordering/index.html", {"foods":Food.objects.all()})
