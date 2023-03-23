from django.urls import path

from incident.views import AllIncidentView, ApproveCompanyIncident, ApproveGeneralIncident, CompanyIncidents, IncidentRetrieveUpdateDeleteView, IncidentView, ReplyUpdateView, ReplyView, TicketRetrieveUpdateView, TicketView, UndoApproveCompanyIncident, UndoApproveGeneralIncident


urlpatterns = [
    path("incident/", IncidentView.as_view(), name="incidents"),
    path("incidents/all/", AllIncidentView.as_view(), name="all_incidents"),
    path("company/incidents/", CompanyIncidents.as_view(), name="all_incidents"),
    path("incident/<str:incident_id>/detail/", IncidentRetrieveUpdateDeleteView.as_view(), name="incident"),
    path("ticket/", TicketView.as_view(), name="tickets"),
    path("ticket/<str:ticket_id>/detail/", TicketRetrieveUpdateView.as_view(), name="ticket"),
    path("reply/", ReplyView.as_view(), name="replies"),
    path("reply/<str:reply_id>/detail/", ReplyUpdateView.as_view(), name="reply"),
    path("company/incident/<str:incident_id>/approve/", ApproveCompanyIncident.as_view()),
    path("general/incident/<str:incident_id>/approve/", ApproveGeneralIncident.as_view()),
    path("company/incident/<str:incident_id>/undo-approve/", UndoApproveCompanyIncident.as_view()),
    path("general/incident/<str:incident_id>/undo-approve/", UndoApproveGeneralIncident.as_view()),
]