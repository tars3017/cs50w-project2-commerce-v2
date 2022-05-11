from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class auction_list(models.Model):
    item = models.CharField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    image = models.URLField(max_length=200)
    desc = models.CharField(max_length=500, default='description example')
    user_watch = models.ManyToManyField(User, blank=True, related_name="") # 05/11 now working

    def __str__(self):
        return f"{self.id}: {self.item} {self.price}$"

class bid(models.Model):
    pass


