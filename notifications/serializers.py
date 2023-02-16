from rest_framework import serializers

from notifications.models import Notification


class NotificationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = (
            "user",
            "id",
            "created_at",
            "updated_at",
        )