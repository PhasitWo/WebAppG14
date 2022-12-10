from django.db import models
# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to = "images/")
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}/{self.price}"

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.username}"

class Order_User(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=10, default="")
    total = models.FloatField(default=0)
    def __str__(self):
        return f"{self.order_id}-{self.user}"

class Order(models.Model):
    order = models.ForeignKey(Order_User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return f"{self.order}--{self.food}--{self.quantity}"