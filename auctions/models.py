from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class auction_list(models.Model):
    item = models.CharField(max_length=64)
    create_date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField(default=0)
    image = models.URLField(max_length=200)
    desc = models.CharField(max_length=500, default='description example')
    current_bid = models.IntegerField(default=price)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="sell_item", default='')
    comment = models.CharField(max_length=500, default='')
    closed = models.BooleanField(default=False)
  
    def __str__(self):
        return f"{self.id}: {self.item} {self.price}$ {self.current_bid}"

class bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="who")
    my_bid = models.IntegerField(default='')
    my_target = models.ForeignKey('auction_list', on_delete=models.CASCADE, related_name='my_target')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} bid {self.my_target.item} for {self.my_bid} dollars at {self.date}"

class watch_list(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user")
    all_list = models.ManyToManyField('auction_list', blank=True, related_name='now_watch')

    def __str__(self):
        return f"{self.id}: {self.user}"

class winner(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="winner")
    win_item = models.ForeignKey('auction_list', on_delete=models.CASCADE, related_name="win_item")

    def __str__(self):
        return f"{self.user} win {self.win_item.item}"