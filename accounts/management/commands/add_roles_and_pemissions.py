from django.core.management.base import BaseCommand

from role.models import Role, RolePermission
from accounts.permissions import permissions, roles


class Command(BaseCommand):

    def add_permissions(self) -> None:
        print("Adding permissions")
        for query in permissions:
            permission, created = RolePermission.objects.get_or_create(**query)

    def add_roles(self) -> None:
        print("Adding roles")
        for query in roles:
            if role := Role.objects.filter(name__iexact=query["name"]).first():
                continue
            else:
                permissions = RolePermission.objects.filter(name__in=query["permissions"]).all()
                role = Role.objects.create(name=query["name"])
                for permission in permissions:
                    role.permissions.add(permission)

    def handle(self, *args, **options):
        print("Started")
        self.add_permissions()
        self.add_roles()
        print("Done")

