from django.urls import path

from accounts.views import AddUser, ChangePassword, CompanySignUp, CustomerSignUp, Login, ResendOtp, SendPhoneNumberOtp, VerifyOtp, VerifyPhoneNumberOtp


urlpatterns = [
    path("register/customer/", CustomerSignUp.as_view()),
    path("register/company/", CompanySignUp.as_view()),
    path("add-user/", AddUser.as_view()),
    path("verify-otp/", VerifyOtp.as_view()),
    path("resend-otp/", ResendOtp.as_view()),
    path("verify-phone-otp/", VerifyPhoneNumberOtp.as_view()),
    path("send-phone-otp/", SendPhoneNumberOtp.as_view()),
    path("login/", Login.as_view()),
    path("change-password/", ChangePassword.as_view()),
]