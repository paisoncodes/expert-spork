from rest_framework import serializers
from accounts.models import User
from accounts_profile.models import CompanyProfile, CompanyUser, Industry, Location, State, UserProfile



class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        user = User.objects.create_user(**validated_data)

        UserProfile.objects.create(user=user,first_name=first_name,last_name=last_name)

        return user
class CompanyRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    state = serializers.CharField()
    company_name = serializers.CharField()
    industry = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "state", "company_name", "industry")

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        state = validated_data.pop("state")
        industry = Industry.objects.filter(name__iexact=validated_data.pop("industry")).first()
        state = State.objects.filter(state__iexact=state).first()
        company_name = validated_data.pop('company_name')
        user = User.objects.create_user(**validated_data)
        user.user_type = User.UserType.COMPANY
        user.save()

        UserProfile.objects.create(user=user,first_name=first_name,last_name=last_name)

        Location.objects.create(name="office", state=state,owner=user)
        
        company = CompanyProfile.objects.create(company_name=company_name, industry=industry, user=user)

        CompanyUser.objects.create(company=company, user=user, is_company_admin=True)

        return user

class AddUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()

class AddUserPassword(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class VerifyTokenSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    email = serializers.EmailField()


class ResendTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class SendPhoneOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(help_text="Example: 2348012345678")


class VerifyPhoneOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()