from email.policy import default
from uuid import uuid4
from rest_framework import serializers

from accounts_profile.models import City, CompanyProfile, CompanyUser, Lga, Location, State, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(
        read_only=True, method_name="get_user_email"
    )
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
        )

    def get_user_email(self, instance):
        return instance.user.email

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
        )

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        exclude = (
            "owner",
            "id",
            "created_at",
            "updated_at",
        )

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        exclude = (
            "id"
        )

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = (
            "id"
        )
class LgaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lga
        exclude = (
            "id"
        )