from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from incident.models import Incident, Ticket, TicketReply

from incident.serializers import IncidentSerializer, TicketReplySerializer, TicketSerializer
from utils.utils import api_response


class IncidentView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IncidentSerializer

    def get(self, request):
        incidents = Incident.objects.filter(owner=request.user)
        serializer = self.serializer_class(incidents, many=True)
        return api_response("Incidents gotten", serializer.data, True, 200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Incident created successfully",serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class IncidentRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IncidentSerializer

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        serializer = self.serializer_class(incident)
        return api_response("Incident retrieved", serializer.data, True, 200)
    
    def put(self, request, incident_id):
        user = get_object_or_404(User, id=request.user.id)
        incident, created = Incident.objects.get_or_create(owner=user, id=incident_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=incident, validated_data=serializer.validated_data)
        return api_response("Incident updated", serializer.data, True, 202)

class TicketView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(owner=request.user)
        serializer = self.serializer_class(tickets, many=True)
        return api_response("Tickets gotten", serializer.data, True, 200)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Ticket registered successfully", serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class TicketRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer

    def get(self, request, ticket_id):
        incident = get_object_or_404(Incident, id=ticket_id)
        serializer = self.serializer_class(incident)
        return api_response("Ticket gotten", serializer.data, True, 200)
    
    def put(self, request, ticket_id):
        user = get_object_or_404(User, id=request.user.id)
        ticket, created = Ticket.objects.get_or_create(owner=user, id=ticket_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        
        serializer.update(instance=ticket, validated_data=serializer.validated_data)
        return api_response("Ticket updated", serializer.data, True, 202)

class ReplyView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketReplySerializer

    def get(self, request, ticket_id):
        replies = TicketReply.objects.filter(ticket__id=ticket_id)
        serializer = self.serializer_class(replies, many=True)
        return api_response("Replies gotten", serializer.data, True, 200)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Reply saved", serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class ReplyUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketReplySerializer

    def put(self, request, reply_id):
        user = get_object_or_404(User, id=request.user.id)
        reply, created = TicketReply.objects.get_or_create(user=user, id=reply_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=reply, validated_data=serializer.validated_data)
        return api_response("Reply saved", serializer.data, True, 202)
