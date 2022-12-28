from email import message
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password

from accounts_profile.models import CompanyProfile
from .permissions import IsCompanyAdminOrBaseAdmin

# from sms.sendchamp import send_sms
from .serializers import (
    AddUserSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ResendTokenSerializer,
    SendPhoneOtpSerializer,
    UserRegistrationSerializer,
    VerifyPhoneOtpSerializer,
    VerifyTokenSerializer,
)
from .models import User
from .otp import get_otp, verify_otp
# from mail.sendinblue import send_email


class CustomerSignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.objects.filter(email=data["email"]).exists():
                return Response(
                    {"message": "User with this email already exists", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            subject = "Please Verify Your Email"
            message = render_to_string(
                "verify_email.html",
                {
                    "user": user,
                    "otp": get_otp(user),
                },
            )
            # mail = send_email(user, html_string=message, subject=subject)

            return Response(
                {
                    "message": "Registration Successful, Check email to verify, otp expires in 5mins"
                    if True
                    else "Registration Successful, Email Sending failed",
                    "status": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
class CompanySignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.objects.filter(email=data["email"]).exists():
                return Response(
                    {"message": "User with this email already exists", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            user.user_type = User.UserType.COMPANY
            user.save()
            subject = "Please Verify Your Email"
            message = render_to_string(
                "verify_email.html",
                {
                    "user": user,
                    "otp": get_otp(user),
                },
            )
            # mail = send_email(user, html_string=message, subject=subject)

            return Response(
                {
                    "message": "Registration Successful, Check email to verify, otp expires in 5mins"
                    if True
                    else "Registration Successful, Email Sending failed",
                    "status": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddUser(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin,]
    serializer_class = AddUserSerializer

    def post(self, request):
        data = request.data 
        data['company'] = CompanyProfile.objects.filter(user=request.user).first()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid:
            serializer.save()

            return Response(
                {
                    "message": "User added successfully",
                    "status": True
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOtp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.data["code"]
            email = serializer.data["email"]
            user = get_object_or_404(User, email=email)
            if verify_otp(user, code):
                user.is_active = True
                user.email_verified = True
                user.save()
                return Response(
                    {"message": "Email verified", "status": True},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Code invalid or expired", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendOtp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResendTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = get_object_or_404(User, email=email)
            if user.is_active:
                return Response(
                    {"message": "Email already verified", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                subject = "Please Verify Your Email"
                message = render_to_string(
                    "verify_email.html",
                    {
                        "user": user,
                        "otp": get_otp(user),
                    },
                )

                # mail = send_email(user, html_string=message, subject=subject)
                return Response(
                    {
                        "message": "Email Sent" if True else "Email not sent",
                        "status": True,
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyPhoneNumberOtp(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyPhoneOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.data["code"]
            user = get_object_or_404(User, pk=request.user.pk)
            if verify_otp(user, code):
                user.is_active = True
                user.phone_verified = True
                user.save()
                return Response(
                    {"message": "Phone Number verified", "status": True},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Code invalid or expired", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SendPhoneNumberOtp(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendPhoneOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone_number = serializer.data["phone_number"]
        user = get_object_or_404(User, pk=request.user.pk)
        user.phone_number = phone_number
        otp = get_otp(user)
        message = f"Your GoCLean code is {otp}"
        # send = send_sms(message=message, phone_number=phone_number)
        if True:
            return Response(
                {"message": "OTP sent to phone number", "status": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Error sending OTP", "status": False},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class Login(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.data
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response(
                {"message": "email or password is incorrect", "status": False},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        current_password = user.password
        check = check_password(data["password"], current_password)

        if check:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login Successful",
                        "data": {
                            "user": {
                                "user_id": user.pk,
                                "email": user.email,
                            },
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                        "status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Account not activated, Please verify your email",
                        "status": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            if user.auth_type == User.AuthType.GOOGLE:
                return Response(
                    {
                        "message": "Please Sign in with Google",
                        "status": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {
                    "message": "email or password is incorrect",
                    "status": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            

class ChangePassword(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, pk=request.user.pk)
        data = serializer.data
        check = check_password(data["old_password"], user.password)
        if check:
            user.password = make_password(data["new_password"])
            user.save()
            return Response(
                {
                    "message": "Password Change Successful",
                    "status": True,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "old password is incorrect",
                "status": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
