from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # watch_list = models.ManyToManyField(auction_list, blank=True, related_name="all_watch") # 05/11 now working  
    pass


class auction_list(models.Model):
    item = models.CharField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    image = models.URLField(max_length=200)
    desc = models.CharField(max_length=500, default='description example')
    watch_user = models.ManyToManyField(User, blank=True, related_name="users")



    def __str__(self):
        return f"{self.id}: {self.item} {self.price}$"

class bid(models.Model):
    pass


