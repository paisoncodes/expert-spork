from django.urls import path

from incident.views import IncidentRetrieveUpdateView, IncidentView, ReplyUpdateView, ReplyView, TicketRetrieveUpdateView, TicketView


urlpatterns = [
    path("incident/", IncidentView.as_view()),
    path("incident/<str:incident_id>/update", IncidentRetrieveUpdateView.as_view()),
    path("ticket/", TicketView.as_view()),
    path("ticket/<str:ticket_id>/update", TicketRetrieveUpdateView.as_view()),
    path("reply/", ReplyView.as_view()),
    path("reply/<str:reply_id>/update", ReplyUpdateView.as_view()),
]