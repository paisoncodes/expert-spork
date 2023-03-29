from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import User
from accounts_profile.models import CompanyUser, Location
from incident.models import Incident, Ticket, TicketAssignee, TicketReply
from accounts.permissions import IsCompanyAdmin, IsVerifiedAndActive

from incident.serializers import IncidentSerializer, IncidentViewSerializer, TicketAssigneeSerializer, TicketReplySerializer, TicketSerializer
from notifications.models import Notification
from subscription.models import ACTIVE, Subscription
from utils.utils import api_response, send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q


state = openapi.Parameter('state', openapi.IN_QUERY,
                             details="State you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
lga = openapi.Parameter('lga', openapi.IN_QUERY,
                             details="Lga you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
search = openapi.Parameter('search', openapi.IN_QUERY,
                             details="Parameter you want to filter by.",
                             type=openapi.TYPE_STRING)
date = openapi.Parameter('date', openapi.IN_QUERY,
                             details="Date you want to filter by.",
                             type=openapi.TYPE_STRING)
alert_type = openapi.Parameter('alert_type', openapi.IN_QUERY,
                             details="Alert type you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
primary_threat_actor = openapi.Parameter('primary_threat_actor', openapi.IN_QUERY,
                             details="Primary Threat Actor you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
impact = openapi.Parameter('impact', openapi.IN_QUERY,
                             details="Impact you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
threat_level = openapi.Parameter('threat_level', openapi.IN_QUERY,
                             details="Threat Level you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
affected_group = openapi.Parameter('affected_group', openapi.IN_QUERY,
                             details="Affected group you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
incident_nature = openapi.Parameter('incident_nature', openapi.IN_QUERY,
                             details="Incident nature you want to filter by.",
                             type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
# incident_nature = openapi.Parameter('incident nature', openapi.IN_QUERY,
#                              details="Incident nature you want to filter by.",
#                              type=openapi.TYPE_STRING)
ticket_id = openapi.Parameter('ticket_id', openapi.IN_QUERY,
                             details="ID of ticket you want to retrieve replies for.",
                             type=openapi.TYPE_STRING, required=True)

class IncidentView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentSerializer

    @swagger_auto_schema(manual_parameters=[state])#, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, threat_level, affected_group])
    def get(self, request):

        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        threat_level = request.GET.get('threat_level', None)
        state = request.GET.get('state', None)
        affected_group = request.GET.get('affected_group', None)
        # city = request.GET.get('city', None)  
        lga = request.GET.get('lga', None)

        query = {"owner": request.user}

        if search:
            query["details__icontains"]=search
        if date:
            query["date"]=date
        if alert_type:
            query["alert_type__name__in"]=alert_type
        if primary_threat_actor:
            query["primary_threat_actor__name__in"]=primary_threat_actor
        if impact:
            query["impact__name__in"]=impact
        if threat_level:
            query["threat_level__name__in"]=threat_level
        if affected_group:
            query["affected_groups__name__in"]=affected_group
        if incident_nature:
            query["incident_nature__name__in"]=incident_nature
        if lga:
            query["lga__lga__in"]=lga
        if state:
            query["state__state__in"]=state
        # if city:
        #     query["city__city__icontains"]=city

        incidents = Incident.objects.filter(**query)

        serializer = IncidentViewSerializer(incidents, many=True)
        return api_response("Incidents gotten", serializer.data, True, 200)

    def post(self, request):
        data = request.data
        data["owner"] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            state = serializer.data["state"]
            alert_type = serializer.data["alert_type"]
            incident_nature = serializer.data["incident_nature"]
            threat_level = serializer.data["threat_level"]
            impact = serializer.data["impact"]
            primary_threat_actor = serializer.data["primary_threat_actor"]
            affected_groups = serializer.data["affected_groups"]
            # city = serializer.data.city
            if subscriptions := Subscription.objects.filter(Q(alert_type__id__in=[alert_type]) | Q(state__id__in=[state]) | Q(incident_nature__id__in=[incident_nature]) | Q(threat_level__id__in=[threat_level]) | Q(impact__id__in=[impact]) | Q(primary_threat_actor__id__in=[primary_threat_actor]) | Q(affected_groups__name__in=affected_groups), status=ACTIVE).distinct():
                for subscription in subscriptions:
                    print(subscription)
                    if subscription.customer == request.user:
                        Notification.objects.create(title="You reported an incident.", user=subscription.customer, object_id=serializer.data["id"])
                        subject = "Incident Report"

                        message = "You reported an incident."

                        send_mail(subscription.customer.email, subject=subject, body=message)
                    else:
                        Notification.objects.create(title="Incident reported. You're getting this because your subscription includes this incident.", user=subscription.customer, object_id=serializer.data["id"])
                        subject = "Incident Report"

                        message = "Incident reported. You're getting this because your subscription includes this incident"

                        send_mail(subscription.customer.email, subject=subject, body=message)

            return api_response("Incident created successfully",serializer.data, True, 201)
        else:
            return api_response("ERROR", serializer.errors, False, 400)


class CompanyIncidents(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentViewSerializer

    @swagger_auto_schema(manual_parameters=[state, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, threat_level, affected_group])
    def get(self, request):
        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        threat_level = request.GET.get('threat_level', None)
        affected_group = request.GET.get('affected_group', None)
        state = request.GET.get('state', None)
        # city = request.GET.get('city', None)  
        lga = request.GET.get('lga', None)

        query = {}
        user_company = CompanyUser.objects.get(user=request.user)

        company_users = CompanyUser.objects.filter(company=user_company.company).values_list('user__id', flat=True)
        if user_company.is_company_admin == True:
            query["owner__id__in"] = company_users
        else:
            query["owner__id__in"] = company_users
            query["company_approved"] = True
        if search:
            query["details__icontains"]=search
        if date:
            query["date"]=date
        if alert_type:
            query["alert_type__name__in"]=alert_type
        if primary_threat_actor:
            query["primary_threat_actor__name__in"]=primary_threat_actor
        if impact:
            query["impact__name__in"]=impact
        if threat_level:
            query["threat_level__name__in"]=threat_level
        if affected_group:
            query["affected_group__name__in"]=affected_group
        if incident_nature:
            query["incident_nature__name__in"]=incident_nature
        if lga:
            query["lga__lga__in"]=lga
        if state:
            query["state__state__in"]=state
        # if city:
        #     query["city__city__icontains"]=city

        incidents = Incident.objects.filter(**query)

        serializer = self.serializer_class(incidents, many=True)

        return api_response("Company Incidents fetched", serializer.data, True, 200)

class ApproveCompanyIncident(GenericAPIView):
    permission_classes = (IsCompanyAdmin,)
    serializer_class = IncidentSerializer

    def put(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.company_approved = True
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class ApproveGeneralIncident(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IncidentSerializer
    def put(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.admin_approved = True
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class UndoApproveCompanyIncident(GenericAPIView):
    permission_classes = (IsCompanyAdmin,)
    serializer_class = IncidentSerializer

    def put(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.company_approved = False
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class UndoApproveGeneralIncident(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = IncidentSerializer
    def put(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        incident.admin_approved = False
        incident.save()

        return api_response("Incident approved", {}, True, 202)

class AllIncidentView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentViewSerializer

    @swagger_auto_schema(manual_parameters=[state, lga, search, date, incident_nature, alert_type, primary_threat_actor, impact, threat_level, affected_group])
    def get(self, request):
        search = request.GET.get('search', None)
        date = request.GET.get('date', None)
        incident_nature = request.GET.get('incident_nature', None)
        alert_type = request.GET.get('alert_type', None)
        primary_threat_actor = request.GET.get('primary_threat_actor', None)
        impact = request.GET.get('impact', None)
        threat_level = request.GET.get('threat_level', None)
        affected_group = request.GET.get('affected_group', None)
        state = request.GET.get('state', None)
        # city = request.GET.get('city', None)
        lga = request.GET.get('lga', None)

        query = {}

        if request.user.is_superuser:
            pass
        else:
            query["admin_approved"] = True
        if search:
            query["details__icontains"]=search
        if date:
            query["date"]=date
        if alert_type:
            query["alert_type__name__in"]=alert_type
        if primary_threat_actor:
            query["primary_threat_actor__name__in"]=primary_threat_actor
        if impact:
            query["impact__name__in"]=impact
        if threat_level:
            query["threat_level__name__in"]=threat_level
        if affected_group:
            query["affected_group__name__in"]=affected_group
        if incident_nature:
            query["incident_nature__name__in"]=incident_nature
        if lga:
            query["lga__lga__in"]=lga
        if state:
            query["state__state__in"]=state
        # if city:
        #     query["city__city__icontains"]=city

        incidents = Incident.objects.filter(**query)
        
        serializer = self.serializer_class(incidents, many=True)
        return api_response("Incidents fetched", serializer.data, True, 200)

class IncidentRetrieveUpdateDeleteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = IncidentSerializer

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, id=incident_id)
        serializer = IncidentViewSerializer(incident)
        return api_response("Incident retrieved", serializer.data, True, 200)
    
    def put(self, request, incident_id):
        if incident:= Incident.objects.filter(id=incident_id).first():
            if incident_owner_company := CompanyUser.objects.filter(user=incident.owner).first():
                is_company_admin = CompanyUser.objects.filter(company=incident_owner_company.company, is_company_admin=True, user=request.user).exists()
            else:
                is_company_admin = False
            if request.user != incident.owner or not request.user.is_superuser or not is_company_admin:
                return api_response("You are not allowed to edit this incident", {}, False, 400)
            serializer = self.serializer_class(data=request.data, partial=True)
            if not serializer.is_valid():
                return api_response("ERROR", serializer.errors, False, 400)
            serializer.update(instance=incident, validated_data=serializer.validated_data)
            return api_response("Incident updated", serializer.data, True, 202)
        return api_response("Incident not found", {}, False, 404)
    
    def delete(self, request, incident_id):
        if incident:= Incident.objects.filter(id=incident_id).first():
            if incident_owner_company := CompanyUser.objects.filter(user=incident.owner).first():
                is_company_admin = CompanyUser.objects.filter(company=incident_owner_company.company, is_company_admin=True, user=request.user).exists()
            else:
                is_company_admin = False
            if request.user != incident.owner or not request.user.is_superuser or not is_company_admin:
                return api_response("You are not allowed to delete this incident", {}, False, 400)
            incident.delete()
            return api_response("Incident deleted", {}, True, 200)
        return api_response("Incident not found", {}, False, 404)

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
            return api_response("ERROR", serializer.errors, False, 400)

class TicketRetrieveUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketSerializer

    def get(self, request, ticket_id):
        incident = get_object_or_404(Ticket, id=ticket_id)
        serializer = self.serializer_class(incident)
        return api_response("Ticket gotten", serializer.data, True, 200)
    
    def put(self, request, ticket_id):
        ticket, created = Ticket.objects.get_or_create(owner=request.user, id=ticket_id)
        if "closed" in request.data.keys() and request.user != ticket.owner:
            return api_response("You are not permitted to close this ticket", {}, False, 400)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
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
                Notification.objects.create(title="Ticket has been responded to.",user=ticket.owner, object_id=ticket.id)
            return api_response("Reply saved", serializer.data, True, 201)
        else:
            return api_response("ERROR", serializer.errors, False, 400)

class ReplyUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsVerifiedAndActive)
    serializer_class = TicketReplySerializer

    def put(self, request, reply_id):
        reply, created = TicketReply.objects.get_or_create(user=request.user, id=reply_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
        serializer.update(instance=reply, validated_data=serializer.validated_data)
        return api_response("Reply saved", serializer.data, True, 202)