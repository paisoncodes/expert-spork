from django.db import models
from accounts.models import BaseModel, User

# Create your models here.

class Package(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    amount = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)