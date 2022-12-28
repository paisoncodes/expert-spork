from email.policy import default
from uuid import uuid4
from rest_framework import serializers

from accounts_profile.models import CompanyProfile, CompanyUser, UserProfile

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
