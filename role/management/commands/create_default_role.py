from django.core.management.base import BaseCommand

from role.models import RolePermission


class Command(BaseCommand):

    def add_default_role_and_permission(self):
        if permission := RolePermission.objects.filter(name__iexact="Add Subscription", method__iexact="POST", module_name__iexact="RolePermission").first():
            pass
        
        pass

    def handle(self, *args, **options):
        print("Started")
        self.add_default_role_and_permission()
        print("Done")

