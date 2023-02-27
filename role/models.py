from django.db import models
from accounts.models import BaseModel, User
from django.db.models import JSONField



class RolePermission(models.Model):
    class PermissionMethod(models.TextChoices):
        GET = "get", "GET"
        POST = "post", "POST"
        PUT = "put", "PUT"
        DELETE = "delete", "DELETE"
    name = models.CharField(max_length=225)
    method = models.CharField(max_length=100, choices=PermissionMethod.choices, default=PermissionMethod.GET)
    module_name = models.CharField(max_length=225)
    
    def __str__(self) -> str:
        return self.name



class Role(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField("RolePermission")

    
    def __str__(self) -> str:
        return self.name

