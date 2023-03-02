
import json
from rest_framework.decorators import api_view
import requests
from accounts.models import User

from accounts_profile.models import Industry, Lga, State, UserProfile
from accounts_profile.serializers import IndustrySerializer, LgaSerializer, StateSerializer
from incident.models import IncidentNature, IncidentType
from incident.serializers import IncidentNatureSerializer, IncidentTypeSerializer
from role.models import Role
from utils.utils import api_response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



@api_view(["GET"])
def populate_state(request):
    try:
        url_1 = "https://api.facts.ng/v1/states/"
        response = requests.request("GET", url_1)
        for state in response.json():
            if not State.objects.filter(state=state["name"]).exists():
                state_ = State.objects.create(state=state["name"])
                lgas = (requests.request("GET", state["uri"])).json()
                for lga in lgas["lgas"]:
                    if not Lga.objects.filter(lga=lga, state=state_).exists():
                        Lga.objects.create(lga=lga, state=state_)
                    continue
            continue
        return api_response("Success", {}, True, 200)
    except Exception as e:
        return api_response(f"An error occured: {str(e)}",{}, False, 400)
    
@api_view(["GET"])
def count_lgas(request):
    data = {}
    states = State.objects.all()
    for state in states:
        data[state.state] = Lga.objects.filter(state=state).count()
    
    return api_response("Success", data, True, 200)

@api_view(["GET"])
def populate_industries(request):
    for industry in ["TECHNOLOGY", "TRANSPORT", "FINANCE", "OTHER"]:
        if not Industry.objects.filter(name=industry).exists():
            Industry.objects.create(name=industry)
            return api_response("Industry Populated", {}, True, 200)
        continue



@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['industry'],
                             properties={
                                 'industry': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_industry(request):
    industry = request.data.get("industry")
    if not Industry.objects.filter(name__iexact=industry).exists():
        Industry.objects.create(name=industry.upper())
        return api_response("Industry Already exists", {}, True, 201)
    return api_response("Industry Added", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['incident_type'],
                             properties={
                                 'incident_type': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_incident_type(request):
    incident_type = request.data.get("incident_type")
    if not IncidentType.objects.filter(name__iexact=incident_type).exists():
        IncidentType.objects.create(name=incident_type.upper())
        return api_response("Incident Type Added", {}, True, 201)
    
    return api_response("Incident Type Already exists", {}, True, 200)
    


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['incident_nature'],
                             properties={
                                 'incident_nature': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_incident_nature(request):
    incident_nature = request.data.get("incident_nature")
    if not IncidentNature.objects.filter(nature__iexact=incident_nature).exists():
        IncidentNature.objects.create(nature=incident_nature.upper())
        return api_response("Incident Nature Added", {}, True, 201)
    return api_response("Incident Nature Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['email'],
                             properties={
                                 'email': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_superadmin(request):
    try:
        email = request.data['email']
        data = {
            "email": email,
            "password": "admin"
        }
        user = User.objects.create_superuser(**data)
        role = Role.objects.filter(name__iexact="Aquiline Admin").first()
        UserProfile.objects.create(user=user, role=role)
        return api_response("Success", {}, True, 201)
    except Exception as e:
        return api_response(f'Error: {str(e)}', {}, False, 200)


@swagger_auto_schema(method='delete', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['email'],
                             properties={
                                 'email': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["DELETE"])
def remove_superadmin(request):
    try:
        email = request.data['email']
        
        User.objects.filter(email=email).delete()
        return api_response("Success", {}, True, 200)
    except Exception as e:
        return api_response(f'Error: {str(e)}', {}, False, 400)


@api_view(["GET"])
def get_states(request):
    states = State.objects.all()
    serialzier = StateSerializer(states, many=True)

    return api_response("States fetched", serialzier.data, True, 200)

state = openapi.Parameter('state', openapi.IN_QUERY,
                             description="State you want to retrieve lgas from.",
                             type=openapi.TYPE_STRING, required=True)

@swagger_auto_schema(manual_parameters=[state], method='get')
@api_view(["GET"])
def get_lgas(request):
    state = request.GET.get('state', None)
    lgas = Lga.objects.filter(state__state__icontains=state)
    serialzier = LgaSerializer(lgas, many=True)

    return api_response("Lgas fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_industries(request):
    industries = Industry.objects.all()
    serialzier = IndustrySerializer(industries, many=True)

    return api_response("Industries fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_incident_type(request):
    incident_types = IncidentType.objects.all()
    serialzier = IncidentTypeSerializer(incident_types, many=True)

    return api_response("Incident Types fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_incident_nature(request):
    incident_natures = IncidentNature.objects.all()
    serialzier = IncidentNatureSerializer(incident_natures, many=True)

    return api_response("Incident Natures fetched", serialzier.data, True, 200)