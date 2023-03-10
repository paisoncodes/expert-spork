from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import User
from accounts_profile.models import CompanyUser, Location
from incident.models import Incident, Ticket, TicketAssignee, TicketReply
from accounts.permissions import IsCompanyAdmin, IsVerifiedAndActive

from incident.serializers import IncidentSerializer, IncidentViewSerializer, TicketAssigneeSerializer, TicketReplySerializer, TicketSerializer
from notifications.models import Notification
from utils.utils import api_response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q


state = openapi.Parameter('state', openapi.IN_QUERY,
                             details="State you want to filter by.",
                             type=openapi.TYPE_STRING)
lga = openapi.Parameter('lga', openapi.IN_QUERY,
                             details="Lga you want to filter by.",
                             type=openapi.TYPE_STRING)
search = openapi.Parameter('search', openapi.IN_QUERY,
                             details="Parameter you want to filter by.",
                             type=openapi.TYPE_STRING)
date = openapi.Parameter('date', openapi.IN_QUERY,
                             details="Date you want to filter by.",
                             type=openapi.TYPE_STRING)
alert_type = openapi.Parameter('alert_type', openapi.IN_QUERY,
                             details="Alert type you want to filter by.",
                             type=openapi.TYPE_STRING)
primary_threat_actor = openapi.Parameter('primary_threat_actor', openapi.IN_QUERY,
                             details="Primary Threat Actor you want to filter by.",
                             type=openapi.TYPE_STRING)
impact = openapi.Parameter('impact', openapi.IN_QUERY,
                             details="Impact you want to filter by.",
                             type=openapi.TYPE_STRING)
advisory = openapi.Parameter('advisory', openapi.IN_QUERY,
                             details="Advisory you want to filter by.",
                             type=openapi.TYPE_STRING)
threat_level = openapi.Parameter('threat_level', openapi.IN_QUERY,
                             details="Threat Level you want to filter by.",
                             type=openapi.TYPE_STRING)
affected_group = openapi.Parameter('affected_group', openapi.IN_QUERY,
                             details="Affected group you want to filter by.",
                             type=openapi.TYPE_STRING)
incident_nature = openapi.Parameter('incident_nature', openapi.IN_QUERY,
                             details="Incident nature you want to filter by.",
                             type=openapi.TYPE_STRING)
# incident_nature = openapi.Parameter('incident nature', openapi.IN_QUERY,
#                              details="Incident nature you want to filter by.",
#                              type=openapi.TYPE_STRING)
ticket_id = openapi.Parameter('ticket_id', openapi.IN_QUERY,
                             details="ID of ticket you want to retrieve replies for.",
                             type=openapi.TYPE_STRING, required=True)

class IncidentView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentSerializer

    @swagger_auto_schema(manual_parameters=[state, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, advisory, threat_level, affected_group])
    def get(self, request):

        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        advisory = request.GET.get('advisory', None)
        threat_level = request.GET.get('threat_level', None)
        state = request.GET.get('state', None)
        affected_group = request.GET.get('affected_group', None)
        # city = request.GET.get('city', None)  
        lga = request.GET.get('lga', None)

        incidents = Incident.objects.filter(owner=request.user)

        if search:
            incidents = incidents.filter(Q(details__icontains=search))
        if date:
            incidents = incidents.filter(date=date)
        if alert_type:
            incidents = incidents.filter(alert_type__name__icontains=alert_type)
        if primary_threat_actor:
            incidents = incidents.filter(primary_threat_actor__name__icontains=primary_threat_actor)
        if impact:
            incidents = incidents.filter(impact__name__icontains=impact)
        if advisory:
            incidents = incidents.filter(advisory__name__icontains=advisory)
        if threat_level:
            incidents = incidents.filter(threat_level__name__icontains=threat_level)
        if affected_group:
            incidents = incidents.filter(affected_group__name__icontains=affected_group)
        if incident_nature:
            incidents = incidents.filter(incident_nature__name__icontains=incident_nature)
        if lga:
            incidents = incidents.filter(lga__lga__icontains=lga)
        if state:
            incidents = incidents.filter(state__state__icontains=state)
        # if city:
        #     incidents = incidents.filter(city__city__icontains=city)

        serializer = IncidentViewSerializer(incidents, many=True)
        return api_response("Incidents gotten", serializer.data, True, 200)

    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            lga = serializer.data["lga"]
            state = serializer.data["state"]
            # city = serializer.data.city
            if user_locations := Location.objects.filter(lga=lga, state=state): #, city=city):
                for location in user_locations:
                    if location.owner == request.user:
                        Notification.objects.create(title=f"You reported an incident, {location.name}", user=location.owner, object_id=serializer.data["id"])
                    Notification.objects.create(title=f"Incident reported at registered location, {location.name}", user=location.owner, object_id=serializer.data["id"])
            return api_response("Incident created successfully",serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)


class CompanyIncidents(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentViewSerializer

    @swagger_auto_schema(manual_parameters=[state, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, advisory, threat_level, affected_group])
    def get(self, request):
        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        advisory = request.GET.get('advisory', None)
        threat_level = request.GET.get('threat_level', None)
        affected_group = request.GET.get('affected_group', None)
        state = request.GET.get('state', None)
        # city = request.GET.get('city', None)  
        lga = request.GET.get('lga', None)

        user_company = CompanyUser.objects.get(user=request.user)

        company_users = CompanyUser.objects.filter(company=user_company.company).values_list('user_id', flat=True)
        if user_company.is_company_admin == True:
            incidents = Incident.objects.filter(owner__id__in=company_users)
        else:
            incidents = Incident.objects.filter(owner__id__in=company_users, company_approved=True)

        serializer = self.serializer_class(incidents, many=True)
        if search:
            incidents = incidents.filter(Q(name__icontains=search) | Q(details__icontains=search))
        if date:
            incidents = incidents.filter(date=date)
        if alert_type:
            incidents = incidents.filter(alert_type__name__icontains=alert_type)
        if primary_threat_actor:
            incidents = incidents.filter(primary_threat_actor__name__icontains=primary_threat_actor)
        if impact:
            incidents = incidents.filter(impact__name__icontains=impact)
        if advisory:
            incidents = incidents.filter(advisory__name__icontains=advisory)
        if threat_level:
            incidents = incidents.filter(threat_level__name__icontains=threat_level)
        if affected_group:
            incidents = incidents.filter(affected_group__name__icontains=affected_group)
        if incident_nature:
            incidents = incidents.filter(incident_nature__name__icontains=incident_nature)
        if lga:
            incidents = incidents.filter(lga__lga__icontains=lga)
        if state:
            incidents = incidents.filter(state__state__icontains=state)
        # if city:
        #     incidents = incidents.filter(city__city__icontains=city)

        return api_response("Company Incidents fetched", serializer.data, True, 200)

class ApproveCompanyIncident(GenericAPIView):
    permission_classes = (IsCompanyAdmin,)
    serializer_class = IncidentSerializer

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.company_approved = True
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class ApproveGeneralIncident(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IncidentSerializer
    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.admin_approved = True
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class UndoApproveCompanyIncident(GenericAPIView):
    permission_classes = (IsCompanyAdmin,)
    serializer_class = IncidentSerializer

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.company_approved = False
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class UndoApproveGeneralIncident(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IncidentSerializer
    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.admin_approved = False
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class AllIncidentView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentViewSerializer

    @swagger_auto_schema(manual_parameters=[state, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, advisory, threat_level, affected_group])
    def get(self, request):
        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        advisory = request.GET.get('advisory', None)
        threat_level = request.GET.get('threat_level', None)
        affected_group = request.GET.get('affected_group', None)
        state = request.GET.get('state', None)
        # city = request.GET.get('city', None)
        lga = request.GET.get('lga', None)
        if request.user.is_superuser:
            incidents = Incident.objects.all()
        else:
            incidents = Incident.objects.filter(admin_approved=True)
        if search:
            incidents = incidents.filter(Q(name__icontains=search) | Q(details__icontains=search))
        if date:
            incidents = incidents.filter(date=date)
        if alert_type:
            incidents = incidents.filter(alert_type__name__icontains=alert_type)
        if primary_threat_actor:
            incidents = incidents.filter(primary_threat_actor__name__icontains=primary_threat_actor)
        if impact:
            incidents = incidents.filter(impact__name__icontains=impact)
        if advisory:
            incidents = incidents.filter(advisory__name__icontains=advisory)
        if threat_level:
            incidents = incidents.filter(threat_level__name__icontains=threat_level)
        if affected_group:
            incidents = incidents.filter(affected_group__name__icontains=affected_group)
        if incident_nature:
            incidents = incidents.filter(incident_nature__name__icontains=incident_nature)
        if lga:
            incidents = incidents.filter(lga__lga__icontains=lga)
        if state:
            incidents = incidents.filter(state__state__icontains=state)
        # if city:
        #     incidents = incidents.filter(city__city__icontains=city)
        
        serializer = self.serializer_class(incidents, many=True)
        return api_response("Incidents fetched", serializer.data, True, 200)

class IncidentRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentSerializer

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        serializer = IncidentViewSerializer(incident)
        return api_response("Incident retrieved", serializer.data, True, 200)
    
    def put(self, request, incident_id):
        incident, created = Incident.objects.get_or_create(owner=request.user, id=incident_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=incident, validated_data=serializer.validated_data)
        return api_response("Incident updated", serializer.data, True, 202)

class AssignTickets(GenericAPIView, IsVerifiedAndActive):
    permission_classes = (IsAdminUser,)

    def put(self, request, ticket_id, user_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        user = get_object_or_404(User, id=user_id)
        TicketAssignee.objects.create(ticket=ticket, assignee=user)

        ticket.assignee = user
        ticket.save()
        return api_response("Ticket (re)assigned", {}, True, 200)

class TicketAssigneeHistoryView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = TicketAssigneeSerializer
    def get(self, request, ticket_id):
        history = TicketAssignee.objects.filter(ticket__id=ticket_id)
        serialier = self.serializer_class(history, manay=True)
        return api_response("Ticket assignee history fetched", {}, True, 200)
    
class TicketView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(owner=request.user)
        serializer = self.serializer_class(tickets, many=True)
        return api_response("Tickets gotten", serializer.data, True, 200)
    
    def post(self, request):
        if "title" not in request.data.keys() or "message" not in request.data.keys():
            return api_response("Please add title and message", {}, False, 400)
        data = request.data
        data["owner"] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Ticket registered successfully", serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class TicketRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketSerializer

    def get(self, request, ticket_id):
        incident = get_object_or_404(Ticket, id=ticket_id)
        serializer = self.serializer_class(incident)
        return api_response("Ticket gotten", serializer.data, True, 200)
    
    def put(self, request, ticket_id):
        ticket, created = Ticket.objects.get_or_create(owner=request.user, id=ticket_id)
        if "closed" in request.data.keys() and request.user.is_superuser == True:
            return api_response("You are not permitted to close a ticket", {}, False, 400)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=ticket, validated_data=serializer.validated_data)
        return api_response("Ticket updated", serializer.data, True, 202)

class ReplyView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketReplySerializer

    @swagger_auto_schema(manual_parameters=[ticket_id])
    def get(self, request):
        ticket_id = request.GET.get('ticket_id')
        replies = TicketReply.objects.filter(ticket__id=ticket_id)
        serializer = self.serializer_class(replies, many=True)
        return api_response("Replies fetched", serializer.data, True, 200)
    
    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            ticket= Ticket.objects.get(id=serializer.data["ticket"])
            if ticket.owner != request.user:
                Notification.objects.create(title="Ticket has been responded to",user=ticket.owner, object_id=ticket.id)
            return api_response("Reply saved", serializer.data, True, 201)
        else:
            return api_response(serializer.errors, {}, False, 400)

class ReplyUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketReplySerializer

    def put(self, request, reply_id):
        reply, created = TicketReply.objects.get_or_create(user=request.user, id=reply_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=reply, validated_data=serializer.validated_data)
        return api_response("Reply saved", serializer.data, True, 202)