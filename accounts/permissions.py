from rest_framework.permissions import BasePermission
from .models import User
from accounts_profile.models import CompanyUser, UserProfile


class IsSuperUser(BasePermission):
    """
    The request is authenticated  and user is superuser and staff.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )

class IsCustomer(BasePermission):
    """
    The request is authenticated  and user is customer.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == User.UserType.CUSTOMER
        )

class IsCompanyAdmin(BasePermission):
    """
    The request is authenticated  and user is company admin.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == User.UserType.COMPANY
            and (CompanyUser.objects.get(user=request.user)).is_company_admin == True
        )

class IsCompanyUser(BasePermission):
    """
    The request is authenticated  and user is company user.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == User.UserType.CUSTOMER
            and CompanyUser.objects.filter(user=request.user).exists()
        )

class IsCompanyAdminOrBaseAdmin(BasePermission):
    """
    The request is authenticated  and user is company admin or base admin.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.user.is_authenticated
                and request.user.is_staff
                and request.user.is_superuser
            ) or 
            (
                request.user.is_authenticated
                and request.user.user_type == User.UserType.COMPANY
                and (CompanyUser.objects.get(user=request.user)).is_company_admin == True
            )
        )

class IsVerifiedAndActive(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.email_verified == True or request.user.is_superuser == True or UserProfile.objects.get(user=request.user).disabled == False or UserProfile.objects.get(user=request.user).deleted == False)

permissions = [
    {
        "name": "Add User",
        "method": "POST",
        "module_name": "User"
    },
    {
        "name": "Update User",
        "method": "PUT",
        "module_name": "User"
    },
    {
        "name": "Update Profile",
        "method": "PUT",
        "module_name": "User"
    },
    {
        "name": "View All Users",
        "method": "GET",
        "module_name": "User"
    },
    {
        "name": "View Company Users",
        "method": "GET",
        "module_name": "User"
    },
    {
        "name": "View Individual Users",
        "method": "DELETE",
        "module_name": "User"
    },
    {
       "name": "View All Corporate Accounts",
       "method": "GET",
       "module_name": "User"
    },
    {
        "name": "Add Company",
        "method": "POST",
        "module_name": "Company"
    },
    {
        "name": "Update Corporate Account",
        "method": "PUT",
        "module_name": "User"
    },
    {
        "name": "Add Incident",
        "method": "POST",
        "module_name": "Incident"
    },
    {
        "name": "Update Incident",
        "method": "PUT",
        "module_name": "Incident"
    },
    {
        "name": "Approve Company Incidents",
        "method": "GET",
        "module_name": "Incident"
    },
    {
        "name": "Approve All Incidents",
        "method": "GET",
        "module_name": "Incident"
    },
    {
        "name": "View All Incidents",
        "method": "GET",
        "module_name": "Incident"
    },
    {
        "name": "View All Incidents by User",
        "method": "GET",
        "module_name": "Incident"
    },
    {
        "name": "View All Incidents by Company",
        "method": "GET",
        "module_name": "Incident"
    },
    {
        "name": "Delete Incidents",
        "method": "DELETE",
        "module_name": "Incident"
    },
    {
        "name": "Delete Incidents by Company",
        "method": "DELETE",
        "module_name": "Incident"
    },
    {
        "name": "Delete Incidents by User",
        "method": "DELETE",
        "module_name": "Incident"
    },
    {
        "name": "View All Roles",
        "method": "GET",
        "module_name": "Role"
    },
    {
        "name": "Add Role",
        "method": "POST",
        "module_name": "Role"
    },
    {
        "name": "Update Role",
        "method": "PUT",
        "module_name": "Role"
    },
    {
        "name": "Delete Role",
        "method": "DELETE",
        "module_name": "Role"
    },
    {
        "name": "View All Roles",
        "method": "GET",
        "module_name": "Role"
    },
    {
        "name": "View User Role",
        "method": "GET",
        "module_name": "Role"
    },
    {
        "name": "Add Subscription",
        "method": "POST",
        "module_name": "Subscription"
    },
    {
        "name": "Update Subscription",
        "method": "PUT",
        "module_name": "Subscription"
    },
    {
        "name": "Delete Subscription",
        "method": "DELETE",
        "module_name": "Subscription"
    },
    {
        "name": "View All Subscriptions",
        "method": "GET",
        "module_name": "Subscription"
    },
    {
        "name": "View Subscriptions by User",
        "method": "GET",
        "module_name": "Subscription"
    },
    {
        "name": "View Subscriptions by Company",
        "method": "GET",
        "module_name": "Subscription"
    },
    {
        "name": "View Invoices",
        "method": "GET",
        "module_name": "Invoice"
    },
    {
        "name": "Add Invoice",
        "method": "POST",
        "module_name": "Invoice"
    },
    {
        "name": "View Invoices by User",
        "method": "GET",
        "module_name": "Invoice"
    },
    {
        "name": "View Invoices by Company",
        "method": "GET",
        "module_name": "Invoice"
    },
    {
        "name": "View All Permissions",
        "method": "GET",
        "module_name": "Permission"
    },
    {
        "name": "View User Permissions",
        "method": "GET",
        "module_name": "Permission"
    }
]

roles = [
    {
        "name": "Aquiline Admin",
        "permissions": [permission["name"] for permission in permissions]
    },
    {
        "name": "Company Admin",
        "permissions": [
            "Add User",
            "Update User",
            "Update Profile",
            "View Company Users",
            "Update Corporate Account",
            "Add Incident",
            "Update Incident",
            "Approve Company Incidents",
            "View All Incidents by Company",
            "View All Incidents by User",
            "View All Incidents",
            "Delete Incidents by Company",
            "Delete Incidents by User",
            "View User Role",
            "Add Subscription",
            "View Subscriptions by Company",
            "View Invoices by Company",
            "View User Permissions"
        ]
    },
    {
        "name": "Company User",
        "permissions": [
            "Update Profile",
            "View Company Users",
            "Add Incident",
            "Update Incident",
            "View All Incidents by Company",
            "View All Incidents by User",
            "View All Incidents",
            "Delete Incidents by User",
            "View User Role",
            "View User Permissions"
        ]
    },
    {
        "name": "Individual User",
        "permissions": [
            "Update Profile",
            "Add Incident",
            "Update Incident",
            "View All Incidents by User",
            "View All Incidents",
            "Delete Incidents by User",
            "View User Role",
            "View User Permissions",
            "Add Subscription",
            "View Subscriptions by User",
            "View Invoices by User",
        ]
    }
]