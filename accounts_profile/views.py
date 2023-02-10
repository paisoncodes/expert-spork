from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from accounts_profile.models import CompanyProfile, UserProfile
from rest_framework.response import Response
from rest_framework import status

from accounts_profile.serializers import CompanyProfileSerializer, UserProfileSerializer
from accounts.models import User
from accounts.permissions import IsCompanyAdmin


class Profile(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = self.serializer_class(instance=profile)
        data = serializer.data
        data["phone_number"] = user.phone_number
        data["phone_verified"] = user.phone_verified
        return Response(
            {
                "message": "Profile Gotten",
                "data": data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.update(instance=profile, validated_data=serializer.validated_data)
        return Response(
            {"message": "Update Successful", "status": True}, status=status.HTTP_200_OK
        )

class CompanyProfileView(GenericAPIView):
    permission_classes = [IsCompanyAdmin]
    serializer_class = CompanyProfileSerializer

    def get(self, request):
        print("user name: ", request.user.first_name)
        company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(instance=company_profile)
        return Response(
            {
                "message": "Business Profile Gotten",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        company_profile, created = CompanyProfile.objects.get_or_create(user=user)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.update(
            instance=company_profile, validated_data=serializer.validated_data
        )
        return Response(
            {"message": "Update Successful", "status": True}, status=status.HTTP_200_OK
        )

