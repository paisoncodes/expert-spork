from django.contrib import admin

from .models import Package, Subscription

admin.site.register(Package)
admin.site.register(Subscription)
