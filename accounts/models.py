from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    class AuthType(models.TextChoices):
        EMAIL = "email", "Email"
        GOOGLE = "google", "Google"
        ADDED = "added", "Added"

    class UserType(models.TextChoices):
        CUSTOMER = "client", "Client"
        COMPANY = "company", "Company"

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=225, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=255, choices=UserType.choices, default=UserType.CUSTOMER
    )
    auth_type = models.CharField(
        max_length=255, choices=AuthType.choices, default=AuthType.EMAIL
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @classmethod
    def get_default_pk(cls):
        user, created = cls.objects.get_or_create(
            username='default user',   
        )
        return created if created else user

class Verification(BaseModel):
    user = models.OneToOneField(
        User, related_name="otp", unique=True, on_delete=models.CASCADE
    )
    code = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email
