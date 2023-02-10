from rest_framework import serializers

from incident.models import Incident, Ticket, TicketReply
from django.core.exceptions import ObjectDoesNotExist


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
