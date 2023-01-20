from django.urls import path

from accounts.views import AddUser, ChangePassword, CompanySignUp, CustomerSignUp, Login, ResendOtp, SendPhoneNumberOtp, VerifyOtp, VerifyPhoneNumberOtp


urlpatterns = [
    path("register/customer/", CustomerSignUp.as_view(), name="customer_signup"),
    path("register/company/", CompanySignUp.as_view(), name="company_signup"),
    path("add-user/", AddUser.as_view(), name="add_user"),
    path("verify-otp/", VerifyOtp.as_view()),
    path("resend-otp/", ResendOtp.as_view()),
    path("verify-phone-otp/", VerifyPhoneNumberOtp.as_view()),
    path("send-phone-otp/", SendPhoneNumberOtp.as_view()),
    path("login/", Login.as_view()),
    path("change-password/", ChangePassword.as_view()),
]