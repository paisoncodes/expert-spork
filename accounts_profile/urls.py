from accounts.views import AddUser, CompanyUserEditView, CompanyUsersView
from accounts_profile.views import Profile, CompanyProfileView

from django.urls import path



urlpatterns = [
    path("user", Profile.as_view(), name="user_profile"),
    path("company", CompanyProfileView.as_view(), name="company_profile"),
    path("company/add-user/", AddUser.as_view(), name="add_user"),
    path("company/view-users/", CompanyUsersView.as_view()),
    path("company/edit-user/<str:user_id>/", CompanyUserEditView.as_view()),
]