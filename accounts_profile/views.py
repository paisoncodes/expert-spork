from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts_profile.models import City, CompanyProfile, Location, State, UserProfile
from rest_framework.response import Response
from rest_framework import status

from accounts_profile.serializers import CitySerializer, CompanyProfileSerializer, CompanyProfileViewSerializer, KycUpdateSerializer, LocationSerializer, LocationViewSerializer, StateSerializer, UserProfileSerializer
from accounts.models import User
from accounts.permissions import IsCompanyAdmin, IsVerifiedAndActive
from utils.utils import api_response


class Profile(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
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
        user = request.user
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

class KycUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = KycUpdateSerializer

    def put(self, request):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        serializer = self.serializer_class(data=request.data)
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
    permission_classes = [IsCompanyAdmin, IsVerifiedAndActive]
    serializer_class = CompanyProfileSerializer

    def get(self, request):
        company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
        serializer = CompanyProfileViewSerializer(instance=company_profile)
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

class LocationView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = LocationSerializer

    def get(self, request):
        user = request.user
        locations = Location.objects.filter(owner=user)
        serializer = LocationViewSerializer(locations, many=True)
        return api_response("Locations fetched", serializer.data, True, 200)
    
    def post(self, request):
        user = request.user
        data = request.data
        data["owner"] = user.id

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return api_response("Location added successfully", serializer.data, True, 201)
        
        return api_response("Failed", serializer.errors, False, 400)


class CityView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CitySerializer

    def get(self, request):
        state = request.GET.get('state')
        cities = City.objects.filter(state__state__icontains=state)
        serializer = self.serializer_class(cities, many=True)

        return api_response("Cities fetched", serializer.data, True, 200)

class StateView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = StateSerializer

    def get(self, request):
        states = State.objects.all()
        serializer = self.serializer_class(states, many=True)

        return api_response("States fetched", serializer.data, True, 200)

