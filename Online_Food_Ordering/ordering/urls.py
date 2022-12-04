from django.urls import path
from . import views
app_name = "ordering"
urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("add", views.add, name="add"),
    path("login", views.login, name ="login")
]