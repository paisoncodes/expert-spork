from accounts.views import AddUser, CompanyUserEditView, CompanyUsersView
from accounts_profile.views import CityView, KycUpdateView, LocationUpdateDeleteView, LocationView, Profile, CompanyProfileView, StateView

from django.urls import path



urlpatterns = [
    path("user/", Profile.as_view(), name="user_profile"),
    path("company/", CompanyProfileView.as_view(), name="company_profile"),
    path("company/add-user/", AddUser.as_view(), name="add_user"),
    path("company/view-users/", CompanyUsersView.as_view()),
    path("company/edit-user/<str:user_id>/", CompanyUserEditView.as_view()),
    path("user/kyc-update/", KycUpdateView.as_view()),
    path("cities/<str:state>/", CityView.as_view()),
    path("states/", StateView.as_view()),
    path("user/locations/", LocationView.as_view()),
    path("user/locations/<str:location_id>/edit/", LocationUpdateDeleteView.as_view()),
]