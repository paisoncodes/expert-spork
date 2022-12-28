from platform import platform
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from accounts.models import User
from accounts.social.google_auth import get_user_data
from rest_framework.response import Response
from accounts.serializers import GoogleAuthSerializer
from rest_framework import status
from uuid import uuid4
from rest_framework.permissions import AllowAny


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class GoogleAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        """
        Gets a token from the frontend and uses it to get user data from google
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        credential = data["credential"]
        platform = data["platform"]
        try:
            user_data = get_user_data(credential, platform)
            user_exists = User.objects.filter(email=user_data["email"]).exists()
            if user_exists:
                user: User = User.objects.get(email=user_data["email"])

                if user.auth_type != User.AuthType.GOOGLE:
                    return Response(
                        {
                            "message": "User with this Email already exists",
                            "status": False,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    {
                        "message": "Login with Google successful",
                        "data": {
                            "user": {
                                "user_id": user.pk,
                                "email": user.email,
                            },
                            **get_tokens_for_user(user),
                        },
                        "status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                user = User.objects.create(
                    email=user_data["email"], password=uuid4().hex + user_data["email"]
                )
                user.auth_type = User.AuthType.GOOGLE
                user.save()

                return Response(
                    {
                        "message": "Registration with Google successful",
                        "data": {
                            "user": {"user_id": user.pk, "email": user.email},
                            **get_tokens_for_user(user),
                        },
                        "status": True,
                    },
                    status=status.HTTP_200_OK,
                )
        except ValueError:
            return Response(
                {
                    "message": "Invalid token",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
