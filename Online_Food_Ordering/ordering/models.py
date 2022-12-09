import re
from django.db import models
# Create your models here.

class Food(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to = "images/")
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}/{self.price}"

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

class Order_User(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
    order = models.ForeignKey(Order_User, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    food = models.ForeignKey(Food , on_delete=models.CASCADE)
    quantity = models.IntegerField()