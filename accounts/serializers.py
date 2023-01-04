from rest_framework import serializers
from accounts.models import User
from accounts_profile.models import CompanyUser, UserProfile



class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    lga = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "state", "city", "lga")

    def create(self, **validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        state = validated_data.pop("state")
        city = validated_data.pop("city")
        lga = validated_data.pop("lga")

        user = User.objects.create_user(**validated_data)

        UserProfile.objects.create(user=user,first_name=first_name,last_name=last_name,state=state,city=city,lga=lga)

        return user

class AddUserSerializer(serializers.ModelSerializer):
    company = serializers.ModelField(model_field=id)
    class Meta:
        model = User
        fields = ("email", "company")
    
    def create(self, **validated_data):
        company = validated_data.pop('company', None)
        user = User.objects.add_user(**validated_data)
        user.auth_type = User.AuthType.ADDED
        user.save()

        UserProfile.objects.create(user=user)

        CompanyUser.objects.create(company=company, user=user)

        return user

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
    phone_number = serializers.CharField()


class VerifyPhoneOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()