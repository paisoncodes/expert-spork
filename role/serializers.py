from rest_framework import serializers

from role.models import Role



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]