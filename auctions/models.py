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
  
    def __str__(self):
        return f"{self.id}: {self.item} {self.price}$"

class bid(models.Model):
    pass


class watch_list(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user")
    all_list = models.ManyToManyField('auction_list', blank=True, related_name='now_watch')

    def __str__(self):
        return f"{self.id}: {self.user}"
