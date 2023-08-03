from django.contrib import admin
from .models import User, auction_listings, bids, comments, connect_two, closed_listings

# Register your models here.

admin.site.register(User)
admin.site.register(auction_listings)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(connect_two)
admin.site.register(closed_listings)