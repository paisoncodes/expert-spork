from datetime import datetime
from django.db import models
from accounts.models import BaseModel, User
# Create your models here.

class Package(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.FloatField(default=0)
    max_no_of_users = models.IntegerField(default=0)
    duration = models.IntegerField(default=1, help_text="Duration of the package in months")
    

    @classmethod
    def get_default_pk(cls):
        package, created = cls.objects.get_or_create(
            name='default package',  
            description = "Default package" 
        )
        return created if created else package
    
    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=Package.get_default_pk)
    extra_user = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self) -> str:
        return f"{self.user.email} {self.package.name} {len(Subscription.objects.filter(user=self.user))}"
    