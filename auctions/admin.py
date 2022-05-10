from django.contrib import admin
from .models import User, auction_list, bid

admin.site.register(User)
admin.site.register(auction_list)
admin.site.register(bid)