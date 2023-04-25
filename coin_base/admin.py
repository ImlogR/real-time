from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Coin)
admin.site.register(CoinUserProfile)
admin.site.register(Transaction)
