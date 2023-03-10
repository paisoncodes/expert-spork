from rest_framework import serializers

from incident.models import Advisory, AffectedGroup, AlertType, Impact, Incident, PrimaryThreatActor, ThreatLevel, Ticket, TicketAssignee, TicketReply, IncidentType, IncidentNature
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
    threat_level = serializers.StringRelatedField()
    affected_groups = serializers.StringRelatedField(many=True)
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

class AdvisorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisory
        fields = "__all__"

class ImpactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impact
        fields = "__all__"

class IncidentNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentNature
        fields = "__all__"

class AffectedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectedGroup
        fields = "__all__"

class ThreatLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatLevel
        fields = "__all__"

class PrimaryThreatActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryThreatActor
        fields = "__all__"

class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = "__all__"