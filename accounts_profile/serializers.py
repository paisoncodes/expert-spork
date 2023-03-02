from email.policy import default
from uuid import uuid4
from rest_framework import serializers

from accounts_profile.models import City, CompanyProfile, CompanyUser, Industry, Lga, Location, State, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(
        read_only=True, method_name="get_user_email"
    )

    class Meta:
        model = UserProfile
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
            "deleted"
        )
        read_only_fields = [
            "phone_number",
        ]

    def get_user_email(self, instance):
        return instance.user.email

class CompanyProfileViewSerializer(serializers.ModelSerializer):
    industry = serializers.StringRelatedField()
    class Meta:
        model = CompanyProfile
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
        )
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
        )

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"

class KycUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["kyc"]

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class LocationViewSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    lga = serializers.StringRelatedField()
    class Meta:
        model = Location 
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = (
            "id",
        )
class LgaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lga
        fields = "__all__"