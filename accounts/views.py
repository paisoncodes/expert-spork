from email import message
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password

from accounts_profile.models import CompanyProfile, CompanyUser, Location, UserProfile
from accounts_profile.serializers import CompanyUserSerializer, UserProfileSerializer
from .permissions import IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive

# from sms.sendchamp import send_sms
from .serializers import (
    AddUserSerializer,
    ChangePasswordSerializer,
    CompanyRegistrationSerializer,
    LoginSerializer,
    ResendTokenSerializer,
    SendPhoneOtpSerializer,
    UserRegistrationSerializer,
    VerifyPhoneOtpSerializer,
    VerifyTokenSerializer,
)
from .models import User
from .otp import get_otp, verify_otp

from utils.utils import api_response, generate_password, send_mail, send_message, validate_phone_number
# from mail.sendinblue import send_email


class CustomerSignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.objects.filter(email=data["email"]).exists():
                return Response(
                    {"message": "User with this email already exists", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            otp = get_otp(user)
            subject = "Please Verify Your Email"
            message = f"Your Aquiline Alerts code is {otp}."
            send_mail(user.email, subject=subject, body=message)
            data = {'message': "User account creation successful", 'otp': otp}
            return api_response("Registration successful", data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)
class CompanySignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanyRegistrationSerializer

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

            otp = get_otp(user)
            
            subject = "Please Verify Your Email"

            message = f"Your Aquiline Alerts code is {otp}."

            send_mail(user.email, subject=subject, body=message)

            data = {'message': "User account creation successful", 'otp': otp}
            return api_response("Registration successful", data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class AddUser(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive]
    serializer_class = AddUserSerializer

    def post(self, request):
        data = request.data
        company = CompanyProfile.objects.filter(user=request.user).first()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = User.objects.create(email=serializer.data["email"], user_type=User.AuthType.ADDED)
            CompanyUser.objects.create(user=user, company=company)
            if request.user.user_type == User.UserType.COMPANY:
                location = Location.objects.get(owner=request.user)
                user_location = location
                user_location.owner = user
                user_location.save()
            user.set_password(generate_password(company.company_name, CompanyUser.objects.filter(company=company).count()))
            user.email_verified = True
            user.save()
            return api_response("User added successfully", {}, True, 200)
        else:
            return api_response(serializer.errors, {}, False, 400)

class CompanyUsersView(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive]
    serializer_class = CompanyUserSerializer

    def get(self, request):
        company = CompanyProfile.objects.filter(user=request.user).first()
        users = CompanyUser.objects.filter(company=company)
        serializer = self.serializer_class(data=users)
        return api_response("Users fetched", serializer.data, True, 200)

class CompanyUserEditView(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive]
    serializer_class = UserProfileSerializer

    def put(self, request, user_id):
        if request.user.is_superuser == True:
            user = get_object_or_404(User, id=user_id)
        else:
            company = CompanyProfile.objects.filter(user=request.user).first()
            user = CompanyUser.objects.filter(company=company, user__id=user_id).first().user
        if not user:
            return api_response("User not found", {}, False, 404)
        user_profile = get_object_or_404(UserProfile, user=user)
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=user_profile, validated_data=serializer.validated_data)
            return api_response("Update successful", {}, True, 200)
        return api_response("An error occured", serializer.errors, False, 400)


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
            if user.email_verified:
                return Response(
                    {"message": "Email already verified", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                otp = get_otp(user)
                subject = "Please Verify Your Email"
                message =  f"Your Aquiline Alerts code is {otp}."

                send_mail(user.email, subject=subject, body=message)
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
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
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
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = SendPhoneOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone_number = serializer.data["phone_number"]
        check_phone = validate_phone_number(phone_number)
        if not check_phone:
            return api_response("Invalid phone number", {}, False, 400)
        user = request.user
        user.phone_number = phone_number
        user.save()
        otp = get_otp(user)
        message = f"Your Aquiline Alerts code is {otp}."

        send_message(phone_number, message, user.email)
        
        return Response(
            {"message": "OTP sent to phone number", "status": True},
            status=status.HTTP_200_OK,
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
            if UserProfile.objects.get(user=user).deleted == True or UserProfile.objects.get(user=user).disabled == True:
                return api_response("Account disabled. Reach out to admin for more details")
            if user.email_verified:
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number
                }

                refresh = RefreshToken.for_user(user)
                data["access_token"] = str(refresh.access_token)
                user_profile = UserProfile.objects.get(user=user)
                data["first_name"] = user_profile.first_name
                data["last_name"] = user_profile.last_name
                data["kyc_uploaded"] = True if user_profile.kyc else False
                data["is_verified"] = user.email_verified
                if company_user := CompanyUser.objects.filter(user=user).first():
                    data["is_company_user"] = True 
                    data["is_company_admin"] = company_user.is_company_admin
                    data["company_name"] = company_user.company.company_name
                return api_response("Login Successful", data, True, 200)
    
            else:
                return Response(
                    {
                        "message": "Account not verified, Please verify your email",
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
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
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
