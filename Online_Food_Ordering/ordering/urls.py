from django.urls import path
from . import views
app_name = "ordering"
urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("add", views.add, name="add"),
    path("login", views.login, name ="login"),
    path("logout", views.logout, name = "logout"),
    path("clear_cart", views.clear_cart, name = "clear_cart"),
    path("delete", views.delete, name = "delete"),
    path("confirm_order", views.confirm_order, name = "confirm_order"),
    path("orders", views.orders, name = "orders")
]