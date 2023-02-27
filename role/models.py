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

    @classmethod
    def get_default_pk(cls):
        permission, created = cls.objects.get_or_create(
            id=1,
            name='default role',  
            module_name = "User"
        )
        return created if created else permission
    
    def __str__(self) -> str:
        return self.name



class Role(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField("RolePermission", default=RolePermission.get_default_pk)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_default_pk(cls):
        role, created = cls.objects.get_or_create(
            id=1,
            name='default role',  
            owner = User.objects.filter(is_superuser=True).first()
        )
        return created if created else role.id
    
    def __str__(self) -> str:
        return self.name

