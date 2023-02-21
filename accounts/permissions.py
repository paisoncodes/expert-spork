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