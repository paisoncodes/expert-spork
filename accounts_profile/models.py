from datetime import time
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import BaseModel, User
from django.contrib.postgres.fields import ArrayField


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    locations = models.JSONField(default=list)
    kyc = models.URLField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    

OTHER = "OTHER"
TECHNOLOGY = "TECHNOLOGY"
TRANSPORT = "TRANSPORT"
MARKETING = "MARKETING"
HEALTH = "HEALTH"

class CompanyProfile(BaseModel):
    class IndustryType(models.TextChoices):
        OTHER = OTHER, OTHER
        TECHNOLOGY = TECHNOLOGY, TECHNOLOGY
        TRANSPORT = TRANSPORT, TRANSPORT
        MARKETING = MARKETING, MARKETING
        HEALTH = HEALTH, HEALTH

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    company_name = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=100, choices=IndustryType.choices, default=IndustryType.OTHER)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lga = models.CharField(max_length=100, blank=True, null=True)

class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    is_company_admin = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.user_type==User.UserType.COMPANY:
        company = CompanyProfile.objects.create(user=instance)
        CompanyUser.objects.create(user=instance, company=company,is_company_admin=True)