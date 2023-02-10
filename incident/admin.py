from django.contrib import admin

from .models import Incident, Ticket, TicketReply


admin.site.register(Incident)
admin.site.register(Ticket)
admin.site.register(TicketReply)
