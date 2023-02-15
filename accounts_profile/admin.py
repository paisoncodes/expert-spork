from django.contrib import admin
from .models import CompanyProfile, UserProfile, CompanyUser, State, City, Lga, Location

admin.site.register(CompanyProfile)
admin.site.register(UserProfile)
admin.site.register(CompanyUser)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Lga)
admin.site.register(Location)
