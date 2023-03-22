from django.contrib import admin

from .models import Incident, Ticket, TicketReply, AlertType, IncidentNature, PrimaryThreatActor, Impact, AffectedGroup, ThreatLevel


admin.site.register(Incident)
admin.site.register(Ticket)
admin.site.register(TicketReply)
admin.site.register(AlertType)
admin.site.register(IncidentNature)
admin.site.register(PrimaryThreatActor)
admin.site.register(Impact)
admin.site.register(AffectedGroup)
admin.site.register(ThreatLevel)