from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive
from role.models import Role, RolePermission
from role.serializers import RolePermisionSerializer, RoleSerializer, RoleViewSerializer

from utils.utils import api_response
from django.shortcuts import get_object_or_404



class RoleView(GenericAPIView):
    permission_classes = (IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive)
    serializer_class = RoleSerializer

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleViewSerializer(roles, many=True)
        return api_response("Roles fetched", serializer.data, True, 200)
    
    def post(self, request):
       data = request.data
       serializer = self.serializer_class(data=data)
       if serializer.is_valid():
           serializer.save()
           return api_response("Roles saved", serializer.data, True, 201)
       else:
           return api_response("ERROR", serializer.errors, False, 400)

class RoleRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive)
    serializer_class = RoleSerializer

    def get(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializer = self.serializer_class(role)
        return api_response("Role retrieved", serializer.data, True, 200)


    def put(self, request, role_id):
        role = get_object_or_404(Role, id=role_id, owner=request.user)
        serializer = self.serializer_class(request.data, partial=True)

        if serializer.is_valid():
            serializer.update(instance=role, validated_data=serializer.validated_data)
            return api_response("Role updated", serializer.data, True, 202)
        return api_response(serializer.errors, {}, False, 400)
    
class RolePermissionsView(GenericAPIView):
    permission_classes = (IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive)
    serializer_class = RolePermisionSerializer

    def get(self, request):
        permissions = RolePermission.objects.all()
        serializer = self.serializer_class(permissions, many=True)
        return api_response("Permissions fetched", serializer.data, True, 200)