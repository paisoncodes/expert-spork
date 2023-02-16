from django.db import models
from accounts.models import BaseModel, User


class State(models.Model):
    state = models.CharField(max_length=225)
    country = models.CharField(max_length=255, default="Nigeria")

    def __str__(self) -> str:
        return self.state

class Lga(models.Model):
    lga = models.CharField(max_length=225)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.lga
    
class City(models.Model):
    city = models.CharField(max_length=225)
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cities"
    
    def __str__(self) -> str:
        return self.city

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    kyc = models.ImageField(upload_to=upload_to, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Industry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Industries'
    
    def __str__(self) -> str:
        return self.name

class CompanyProfile(BaseModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    company_name = models.CharField(max_length=200, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.company_name

class CompanyUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    is_company_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email


class Location(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return self.name