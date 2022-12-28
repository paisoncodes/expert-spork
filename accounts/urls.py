from django.urls import path

from accounts.views import CustomerSignUp


urlpatterns = [
    path("register/customer/", CustomerSignUp.as_view())
]