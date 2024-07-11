from django.contrib import admin
from .models import CustomUser, ReceiveOrder

admin.site.register(CustomUser)
admin.site.register(ReceiveOrder)