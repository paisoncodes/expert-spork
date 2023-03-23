from rest_framework import serializers

from role.models import Role, RolePermission



class RolePermisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"
        read_only_fields = [
            "id"
        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
class RoleViewSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField(many=True)
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]