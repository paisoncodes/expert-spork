from rest_framework import serializers

from incident.models import Incident, Ticket, TicketAssignee, TicketReply, IncidentType, IncidentNature
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
class IncidentViewSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    lga = serializers.StringRelatedField()
    incident_nature = serializers.StringRelatedField()
    alert_type = serializers.StringRelatedField()
    primary_threat_actor = serializers.StringRelatedField()
    impact = serializers.StringRelatedField()
    advisory = serializers.StringRelatedField()
    threat_level = serializers.StringRelatedField()
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