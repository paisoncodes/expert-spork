from django.db import models
from accounts.models import BaseModel, User
from django.db.models import JSONField



class Role(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    name = models.CharField(max_length=200)
    permissions = JSONField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)