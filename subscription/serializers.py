from rest_framework import serializers

from subscription.models import Invoice, Package, Subscription



class SubscriptionSerializer(serializers.Serializer):

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = [
            "id",
            "payment_status",
            "status"
        ]
class SubscriptionViewSerializer(serializers.Serializer):
    alert_type = serializers.StringRelatedField(many=True)
    state = serializers.StringRelatedField(many=True)
    incident_nature = serializers.StringRelatedField(many=True)
    primary_threat_actor = serializers.StringRelatedField(many=True)
    impact = serializers.StringRelatedField(many=True)
    threat_level = serializers.StringRelatedField(many=True)
    affected_groups = serializers.StringRelatedField(many=True)
    customer = serializers.StringRelatedField(many=True)
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = [
            "id",
            "payment_status",
            "status"
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
class InvoiceSerializer(serializers.Serializer):
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = [
            "id",
            "date_created",
            "date_from",
            "date_to",
            "paid",
            "amount",
            "number_of_users",
            "invoice_number",
        ]
class InvoiceViewSerializer(serializers.Serializer):
    customer = serializers.StringRelatedField()
    subscription = serializers.StringRelatedField()
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = [
            "id",
            "date_created",
            "date_from",
            "date_to",
            "paid",
            "amount",
            "number_of_users",
            "invoice_number",
        ]