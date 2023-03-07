from django.core.management.base import BaseCommand

from role.models import Role, RolePermission


class Command(BaseCommand):

    def add_default_role_and_permission(self) -> None:
        if role := Role.objects.filter(name__iexact="Default Role").first():
            role.permissions.add(RolePermission.objects.create(name="Add Subscription", method="POST", module_name="Role"))
        else:
            role = Role.objects.create(name="Default Role")
            role.permissions.add(RolePermission.objects.create(name="Add Subscription", method="POST", module_name="Role"))

    def handle(self, *args, **options):
        print("Started")
        self.add_default_role_and_permission()
        print("Done")

