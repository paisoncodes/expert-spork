from django.contrib import admin

from .models import Notification, Messages, Emails
# Register your models here.

admin.site.register(Notification)
admin.site.register(Messages)
admin.site.register(Emails)