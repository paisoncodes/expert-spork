from rest_framework import serializers

from subscription.models import Package, Subscription



class SubscriptionSerializer(serializers.Serializer):

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class PackageSerializer(serializers.Serializer):
    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]