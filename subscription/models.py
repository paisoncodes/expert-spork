from django.db import models
from accounts.models import BaseModel, User

# Create your models here.

class Package(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.FloatField(default=0)
    no_of_subscribers = models.IntegerField(default=0)
    onwer = models.ForeignKey(User, on_delete=models.CASCADE, default=User.get_default_pk)

    @classmethod
    def get_default_pk(cls):
        package, created = cls.objects.get_or_create(
            name='default package',  
            description = "Default package" 
        )
        return created if created else package


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=Package.get_default_pk)
    duration = models.IntegerField(default=30)
    active = models.BooleanField(default=True)