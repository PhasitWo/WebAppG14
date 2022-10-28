from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
items = [[1, 2, 3],[4,5,6]]
def index(request):
    return render(request, "ordering/index.html", {"items":items})
