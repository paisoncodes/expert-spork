from django.contrib import admin
from .models import CompanyProfile, UserProfile, CompanyUser

admin.site.register(CompanyProfile)
admin.site.register(UserProfile)
admin.site.register(CompanyUser)
