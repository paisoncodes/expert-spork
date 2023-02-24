from django.urls import path

from incident.views import AllIncidentView, ApproveCompanyIncident, ApproveGeneralIncident, CompanyIncidents, IncidentRetrieveUpdateView, IncidentView, ReplyUpdateView, ReplyView, TicketRetrieveUpdateView, TicketView


urlpatterns = [
    path("incident/", IncidentView.as_view(), name="incidents"),
    path("incidents/all/", AllIncidentView.as_view(), name="all_incidents"),
    path("company/incidents/", CompanyIncidents.as_view(), name="all_incidents"),
    path("incident/<str:incident_id>/detail/", IncidentRetrieveUpdateView.as_view(), name="incident"),
    path("ticket/", TicketView.as_view(), name="tickets"),
    path("ticket/<str:ticket_id>/detail/", TicketRetrieveUpdateView.as_view(), name="ticket"),
    path("reply/", ReplyView.as_view(), name="replies"),
    path("reply/<str:reply_id>/detail/", ReplyUpdateView.as_view(), name="reply"),
    path("company/incident/<str:incident_id>/approve/", ApproveCompanyIncident.as_view()),
    path("general/incident/<str:incident_id>/approve/", ApproveGeneralIncident.as_view()),
]