from accounts.views import AddUser, AdminCompanyUserEditView, AllCompaniesView, AllCustomersView, AllUsersView, CompanyUsersView
from accounts_profile.views import ChangeUserRoleView, CityView, KycUpdateView, LocationUpdateDeleteView, LocationView, Profile, CompanyProfileView, StateView

from django.urls import path



urlpatterns = [
    path("user/", Profile.as_view(), name="user_profile"),
    path("company/", CompanyProfileView.as_view(), name="company_profile"),
    path("company/add-user/", AddUser.as_view(), name="add_user"),
    path("company/view-users/", CompanyUsersView.as_view()),
    path("admin/view-all-users/", AllUsersView.as_view()),
    path("admin/view-all-customers/", AllCustomersView.as_view()),
    path("admin/view-all-companies/", AllCompaniesView.as_view()),
    path("edit-user/<str:user_id>/", AdminCompanyUserEditView.as_view()),
    path("user/kyc-update/", KycUpdateView.as_view()),
    path("cities/<str:state>/", CityView.as_view()),
    path("states/", StateView.as_view()),
    path("user/locations/", LocationView.as_view()),
    path("user/locations/<str:location_id>/edit/", LocationUpdateDeleteView.as_view()),
    path("user/role/<str:user_id>/update/", ChangeUserRoleView.as_view()),
]