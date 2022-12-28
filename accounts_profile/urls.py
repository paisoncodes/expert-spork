from accounts_profile.views import Profile, CompanyProfileView

from django.urls import path



urlpatterns = [
    path("user", Profile.as_view(), name="user_profile"),
    path("company", CompanyProfileView.as_view(), name="company_profile"),
]