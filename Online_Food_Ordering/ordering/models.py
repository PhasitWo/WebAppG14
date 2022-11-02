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
