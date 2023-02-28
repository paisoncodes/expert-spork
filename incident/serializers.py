from rest_framework import serializers

from incident.models import Incident, Ticket, TicketAssignee, TicketReply, IncidentType, IncidentNature
from django.core.exceptions import ObjectDoesNotExist


class IncidentSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    lga = serializers.StringRelatedField()
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

class TicketAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAssignee
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

class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentType
        fields = "__all__"

class IncidentNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentNature
        fields = "__all__"