from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    kyc = models.URLField(blank=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    locations = ArrayField(models.ForeignKey("Location", related_name="locations", on_delete=models.DO_NOTHING), blank=True, null=True)
    
class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)

NONE = "NONE"
TECHNOLOGY = "TECNOLOGY"
TRANSPORT = "TRANSPORT"
MARKETING = "MARKETING"
HEALTH = "HEALTH"

class Company(models.Model):
    INDUSTRIES = (
        (NONE, NONE),
        (TECHNOLOGY, TECHNOLOGY),
        (TRANSPORT, TRANSPORT),
        (MARKETING, MARKETING),
        (HEALTH, HEALTH),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, choices=INDUSTRIES, default=NONE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
