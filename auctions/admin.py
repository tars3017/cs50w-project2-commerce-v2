from django.contrib import admin
from .models import User, auction_list, bid, watch_list, winner

admin.site.register(User)
admin.site.register(auction_list)
admin.site.register(bid)
admin.site.register(watch_list)
admin.site.register(winner)