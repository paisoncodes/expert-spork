from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password

from accounts_profile.models import CompanyProfile, CompanyUser, Location, UserProfile
from accounts_profile.serializers import CompanyUserSerializer, UserProfileSerializer
from role.models import Role
from role.serializers import RoleViewSerializer
from .permissions import IsVerifiedAndActive

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
from drf_yasg.utils import swagger_auto_schema
from utils.query_params import customer_id


class CustomerSignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(operation_summary="Individual Customer Registration.")
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
            return api_response("ERROR", serializer.errors, False, 400)
class CompanySignUp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanyRegistrationSerializer

    @swagger_auto_schema(operation_summary="Company Registration.")
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
            return api_response("ERROR", serializer.errors, False, 400)

class AddUser(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = AddUserSerializer

    @swagger_auto_schema(operation_summary="Add User.")
    def post(self, request):
        data = request.data
        company = CompanyProfile.objects.filter(user=request.user).first()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = User.objects.create(email=serializer.data["email"], auth_type=User.AuthType.ADDED, user_type=User.UserType.COMPANY if company else User.UserType.CUSTOMER)
            if company:
                CompanyUser.objects.create(user=user, company=company)
            role = Role.objects.filter(name__iexact=serializer.data["role"]).first()
            UserProfile.objects.create(user=user, role=role)
            if request.user.user_type == User.UserType.COMPANY:
                locations = Location.objects.filter(owner=request.user)
                for location in locations:
                    Location.objects.create(owner=user, name=location.name, address=location.address, state=location.state, lga=location.lga)
            count = User.objects.all().count()
            password = generate_password(serializer.data["email"], count)
            user.set_password(password)
            user.email_verified = True
            user.save()
            message = f"An account has been created for you on Aquiline Alerts by {company.company_name}. Below are your account details: \n    {user.email}\n    {password}"
            send_mail(user.email, "Account creation", message)
            return api_response("User added successfully", {}, True, 200)
        else:
            return api_response("ERROR", serializer.errors, False, 400)

class CompanyUsersView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(manual_parameters=[customer_id], operation_summary="View all users in a Company.")
    def get(self, request):
        if request.user.is_superuser:
            company_id = request.GET.get('company_id', None)
            if not company_id:
                return api_response("ERROR", {'message': 'Invalid company id'}, False, 400)
            else:
                company = get_object_or_404(CompanyProfile, id=company_id)
        else:
            company = CompanyProfile.objects.filter(user=request.user).first()
        company_users = CompanyUser.objects.filter(company=company)
        data = {
            "company_name": company.company_name,
            "users": []
        }
        for company_user in company_users:
            user_profile = UserProfile.objects.filter(user__email=company_user.user.email).first()
            user_data = (self.serializer_class(user_profile)).data
            user_data["id"] = company_user.user.id
            if user_profile:
                user_data["has_profile"] = True
            else:
                user_data["has_profile"] = False
            data["users"].append(user_data)
        return api_response("Users fetched", data, True, 200)

class AllUsersView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(operation_summary="View all users in the system.")
    def get(self, request):
        users = User.objects.all()
        data = {"users": []}
        for user in users:
            user_profile = UserProfile.objects.filter(user__email=user.email).first()
            user_data = (self.serializer_class(user_profile)).data
            user_data["id"] = user.id
            if user_profile:
                user_data["has_profile"] = True
            else:
                user_data["has_profile"] = False
            data["users"].append(user_data)
        return api_response("Users fetched", data, True, 200)

class AllCustomersView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(operation_summary="View all individual users in the system.")
    def get(self, request):
        users = User.objects.all().exclude(user_type=User.UserType.COMPANY)
        data = {'users': []}
        for user in users:
            user_profile = UserProfile.objects.filter(user__email=user.email).first()
            user_data = (self.serializer_class(user_profile)).data
            user_data["id"] = user.id
            if user_profile:
                user_data["has_profile"] = True
            else:
                user_data["has_profile"] = False
            data["users"].append(user_data)
        return api_response("Users fetched", data, True, 200)

class AllCompaniesView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(operation_summary="View all companies and their users in the system.")
    def get(self, request):
        companies = CompanyProfile.objects.all()
        data = {'users': []}
        for company in companies:
            company_users = CompanyUser.objects.filter(company=company)
        
            data["company_name"] = company.company_name
            data["company_users"] = []
            for company_user in company_users:
                user_profile = UserProfile.objects.filter(user__email=company_user.user.email).first()
                user_data = (self.serializer_class(user_profile)).data
                user_data["id"] = company_user.user.id
                data["company_users"].append(user_data)
        return api_response("Users fetched", data, True, 200)

class AllCompanyAdminsView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CompanyUserSerializer

    @swagger_auto_schema(operation_summary="View all company admins in the system")
    def get(self, request):
        company_admins = CompanyUser.objects.filter(is_company_admin=True)
        serializer = self.serializer_class(company_admins, many=True)
        data = serializer.data
        for datum in data:
            profile = UserProfile.objects.get(user__id=datum["user"])
            company = CompanyProfile.objects.get(id=datum["company"])
            if profile.first_name and profile.last_name:
                datum["name"] = profile.first_name + " " + profile.last_name
            else:
                datum["name"] = profile.user.email
            datum["company_name"] = company.company_name
        return api_response("Users fetched", data, True, 200)


class AdminCompanyUserEditView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(operation_summary="Update Users by Company/Super admin.")
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
        return api_response("ERROR", serializer.errors, False, 400)


class VerifyOtp(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyTokenSerializer

    @swagger_auto_schema(operation_summary="Verify OTP.")
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

    @swagger_auto_schema(operation_summary="Resend OTP.")
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

    @swagger_auto_schema(operation_summary="Verify Phone OTP.")
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

    @swagger_auto_schema(operation_summary="Send Phone OTP.")
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

    @swagger_auto_schema(operation_summary="Login.")
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
            if UserProfile.objects.get(user=user).disabled == True:
                return api_response("Account disabled. Reach out to admin for more details", {}, False, 400)
            if user.email_verified:
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number
                }

                refresh = RefreshToken.for_user(user)
                data["access_token"] = str(refresh.access_token)
                user_profile = UserProfile.objects.filter(user=user).first()
                if user_profile:
                    data["first_name"] = user_profile.first_name
                    data["last_name"] = user_profile.last_name
                    data["kyc_uploaded"] = True if user_profile.kyc else False
                    data["is_verified"] = user.email_verified
                    data["role"] = RoleViewSerializer(user_profile.role).data
                if company_user := CompanyUser.objects.filter(user=user).first():
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

    @swagger_auto_schema(operation_summary="Change Password.")
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
