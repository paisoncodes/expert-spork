from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import User

from accounts.permissions import IsVerifiedAndActive
from accounts_profile.models import UserProfile
from role.models import Role, RolePermission
from role.serializers import RolePermisionSerializer, RoleSerializer, RoleViewSerializer

from utils.utils import api_response
from django.shortcuts import get_object_or_404



class RoleView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = RoleSerializer

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleViewSerializer(roles, many=True)
        return api_response("Roles fetched", serializer.data, True, 200)
    
    def post(self, request):
       data = request.data
       if role:= Role.objects.filter(name__iexact=data["name"]).first():
           serializer = RoleViewSerializer(role)
           return api_response("Role with this name exists. Try updatingit.", serializer.data, True, 200)
       serializer = self.serializer_class(data=data)
       if serializer.is_valid():
           serializer.save()
           role = Role.objects.all().last()
           serializer = RoleViewSerializer(role)
           return api_response("Roles saved", serializer.data, True, 201)
       else:
           return api_response("ERROR", serializer.errors, False, 400)


class RoleRetrieveUpdateDeleteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = RoleSerializer

    def get(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializer = self.serializer_class(role)
        return api_response("Role retrieved", serializer.data, True, 200)


    def put(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializer = self.serializer_class(request.data, partial=True)

        if serializer.is_valid():
            serializer.update(instance=role, validated_data=serializer.validated_data)
            return api_response("Role updated", serializer.data, True, 202)
        return api_response("ERROR", serializer.errors, False, 400)
    
    def delete(self, request, role_id):
        if role:= Role.objects.filter(id=role_id).first():
            role.delete()
            return api_response("Role deleted", None, True, 204)
        return api_response("Role not found", None, False, 404)
    
class RolePermissionsView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = RolePermisionSerializer

    def get(self, request):
        permissions = RolePermission.objects.all()
        serializer = self.serializer_class(permissions, many=True)
        return api_response("Permissions fetched", serializer.data, True, 200)
    
    def post(self, request):
        data = request.data
        if permission:= RolePermission.objects.filter(name__iexact=data["name"]).first():
            serializer = self.serializer_class(permission)
            return api_response("Permission with this name exists. Try updating it.", serializer.data, True, 200)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            permission = RolePermission.objects.all().last()
            serializer = self.serializer_class(permission)
            return api_response("Permissions saved", serializer.data, True, 201)
        else:
            return api_response("ERROR", serializer.errors, False, 400)

class UserRoleAndPermissionsView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = RoleViewSerializer
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        serializer = self.serializer_class(user_profile.role)
        return api_response("User Role fetched", serializer.data, True, 200)

class RolePermissionRetrieveUpdateDeleteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = RolePermisionSerializer

    def get(self, request, permission_id):
        permission = get_object_or_404(RolePermission, id=permission_id)
        serializer = self.serializer_class(permission)
        return api_response("Permission retrieved", serializer.data, True, 200)


    def put(self, request, permission_id):
        permission = get_object_or_404(RolePermission, id=permission_id)
        serializer = self.serializer_class(request.data, partial=True)

        if serializer.is_valid():
            serializer.update(instance=permission, validated_data=serializer.validated_data)
            return api_response("Permission updated", serializer.data, True, 202)
        return api_response("ERROR", serializer.errors, False, 400)
    
    def delete(self, request, permission_id):
        if permission:= RolePermission.objects.filter(id=permission_id).first():
            permission.delete()
            return api_response("Permission deleted", None, True, 204)
        return api_response("Permission not found", None, False, 404)
    