
import json
from rest_framework.decorators import api_view
import requests
from accounts.models import User

from accounts_profile.models import Industry, Lga, State, UserProfile
from accounts_profile.serializers import IndustrySerializer, LgaSerializer, StateSerializer
from incident.models import Advisory, AffectedGroup, AlertType, Impact, IncidentNature, IncidentType, PrimaryThreatActor, ThreatLevel
from incident.serializers import AdvisorySerializer, AffectedGroupSerializer, AlertTypeSerializer, ImpactSerializer, IncidentNatureSerializer, PrimaryThreatActorSerializer, ThreatLevelSerializer
from role.models import Role
from utils.schedulers import scheduler, subscription_trigger
from utils.utils import api_response, check_subscription_status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def start_job():
    scheduler.add_job(
        check_subscription_status,
        trigger=subscription_trigger,
        name="Check Subscription Status",
    )
    scheduler.start()

start_job()

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
                             required=['alert_type'],
                             properties={
                                 'alert_type': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_alert_type(request):
    alert_type = request.data.get("alert_type")
    definition = request.data.get("definition", "")
    if not AlertType.objects.filter(name__iexact=alert_type).exists():
        AlertType.objects.create(name=alert_type.upper(), definition=definition)
        return api_response("Alert Type Added", {}, True, 201)
    
    return api_response("Alert Type Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['primary_threat_actor'],
                             properties={
                                 'primary_threat_actor': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_primary_threat_actor(request):
    primary_threat_actor = request.data.get("primary_threat_actor")
    definition = request.data.get("definition", "")
    if not PrimaryThreatActor.objects.filter(name__iexact=primary_threat_actor).exists():
        PrimaryThreatActor.objects.create(name=primary_threat_actor.upper(), definition=definition)
        return api_response("Primary Threat Actor Added", {}, True, 201)
    
    return api_response("Primary Threat Actor Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['impact'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_impact(request):
    impact = request.data.get("impact")
    definition = request.data.get("definition", "")
    if not Impact.objects.filter(name__iexact=impact).exists():
        Impact.objects.create(name=impact.upper(), definition=definition)
        return api_response("Impact Added", {}, True, 201)
    
    return api_response("Impact Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['advisory'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_advisory(request):
    advisory = request.data.get("advisory")
    definition = request.data.get("definition", "")
    if not Advisory.objects.filter(name__iexact=advisory).exists():
        Advisory.objects.create(name=advisory.upper(), definition=definition)
        return api_response("Advisory Added", {}, True, 201)
    
    return api_response("Advisory Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['threat_level'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_threat_level(request):
    threat_level = request.data.get("threat_level")
    definition = request.data.get("definition", "")
    if not ThreatLevel.objects.filter(name__iexact=threat_level).exists():
        ThreatLevel.objects.create(name=threat_level.upper(), definition=definition)
        return api_response("Threat Level Added", {}, True, 201)
    
    return api_response("Threat Level Already exists", {}, True, 200)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['primary_threat_actor'],
                             properties={
                                 'primary_threat_actor': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_primary_threat_actor(request):
    primary_threat_actor = request.data.get("primary_threat_actor")
    definition = request.data.get("definition", "")
    if not PrimaryThreatActor.objects.filter(name__iexact=primary_threat_actor).exists():
        PrimaryThreatActor.objects.create(name=primary_threat_actor.upper(), definition=definition)
        return api_response("Primary Threat Actor Added", {}, True, 201)
    
    return api_response("Primary Threat Actor Already exists", {}, True, 200)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['affected_group'],
                             properties={
                                 'affected_group': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["POST"])
def add_affected_group(request):
    affected_group = request.data.get("affected_group")
    definition = request.data.get("definition", "")
    if not AffectedGroup.objects.filter(name__iexact=affected_group).exists():
        AffectedGroup.objects.create(name=affected_group.upper(), definition=definition)
        return api_response("Group Added", {}, True, 201)
    
    return api_response("Group Already exists", {}, True, 200)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['incident_nature'],
                             properties={
                                 'incident_nature': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_incident_nature(request, incident_nature_id):
    if incident_nature:= IncidentNature.objects.filter(id=incident_nature_id).first():
        serializer = IncidentNatureSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=incident_nature, validated_data=serializer.validated_data)
        return api_response("Incident Nature Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 400)

@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['industry'],
                             properties={
                                 'industry': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_industry(request, industry_id):
    if industry:= Industry.objects.filter(id=industry_id).first():
        serializer = IndustrySerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=industry, validated_data=serializer.validated_data)
        return api_response("Industry Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 400)

@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['alert_type'],
                             properties={
                                 'alert_type': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_alert_type(request, alert_type_id):
    if alert_type:= AlertType.objects.filter(id=alert_type_id).first():
        serializer = AlertTypeSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=alert_type, validated_data=serializer.validated_data)
        return api_response("Alert Type Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 400)

@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['affected_group'],
                             properties={
                                 'affected_group': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_affected_group(request, affected_group_id):
    if affected_group:= AffectedGroup.objects.filter(id=affected_group_id).first():
        serializer = AffectedGroupSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(serializer.errors, {}, False, 400)
        serializer.update(instance=affected_group, validated_data=serializer.validated_data)
        return api_response("Affected Group Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 400)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['primary_threat_actor'],
                             properties={
                                 'primary_threat_actor': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_primary_threat_actor(request, threat_actor_id):
    if threat_actor:= PrimaryThreatActor.objects.filter(id=threat_actor_id).first():
        serializer = PrimaryThreatActorSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
        serializer.update(instance=threat_actor, validated_data=serializer.validated_data)
        return api_response("Threat Actor Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 404)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['impact'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_impact(request, impact_id):
    if impact:= Impact.objects.filter(id=impact_id).first():
        serializer = ImpactSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
        serializer.update(instance=impact, validated_data=serializer.validated_data)
        return api_response("Impact Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 404)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['advisory'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_advisory(request, advisory_id):
    if advisory:= Advisory.objects.filter(id=advisory_id).exists():
        serializer = AdvisorySerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
        serializer.update(instance=advisory, validated_data=serializer.validated_data)
        return api_response("Advisory Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 404)


@swagger_auto_schema(method='put', request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['threat_level'],
                             properties={
                                 'impact': openapi.Schema(type=openapi.TYPE_STRING),
                                 'definition': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),)
@api_view(["PUT"])
def update_threat_level(request, threat_level_id):
    if threat_level:= ThreatLevel.objects.filter(id=threat_level_id).first():
        serializer = ThreatLevelSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response("ERROR", serializer.errors, False, 400)
        serializer.update(instance=threat_level, validated_data=serializer.validated_data)
        return api_response("Threat Level Updated", {}, True, 202)
    
    return api_response("Invalid request", {}, False, 404)


@api_view(["DELETE"])
def delete_alert_type(request, alert_type_id):
    if alert_type:= AlertType.objects.filter(id=alert_type_id).first():
        alert_type.delete()
        return api_response("Alert Type Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)


@api_view(["DELETE"])
def delete_affected_group(request, affected_group_id):
    if affected_group:= AffectedGroup.objects.filter(id=affected_group_id).first():
        affected_group.delete()
        return api_response("Affected Group Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)



@api_view(["DELETE"])
def delete_primary_threat_actor(request, threat_actor_id):
    if threat_actor:= PrimaryThreatActor.objects.filter(id=threat_actor_id).first():
        threat_actor.delete()
        return api_response("Threat Actor Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)



@api_view(["DELETE"])
def delete_impact(request, impact_id):
    if impact:= Impact.objects.filter(id=impact_id).first():
        impact.delete()
        return api_response("Impact Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)


@api_view(["DELETE"])
def delete_advisory(request, advisory_id):
    if advisory:= Advisory.objects.filter(id=advisory_id).exists():
        advisory.delete()
        return api_response("Advisory Deleted", {}, True, 202)
    
    return ("Not Found", {}, False, 404)


@api_view(["DELETE"])
def delete_threat_level(request, threat_level_id):
    if threat_level:= ThreatLevel.objects.filter(id=threat_level_id).first():
        threat_level.delete()
        return api_response("Threat Level Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)

@api_view(["DELETE"])
def delete_industry(request, industry_id):
    if industry:= Industry.objects.filter(id=industry_id).first():
        industry.delete()
        return api_response("Industry Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)

@api_view(["DELETE"])
def delete_incident_nature(request, incident_nature_id):
    if incident_nature:= IncidentNature.objects.filter(id=incident_nature_id).first():
        incident_nature.delete()
        return api_response("Incident Nature Deleted", {}, True, 202)
    
    return api_response("Not Found", {}, False, 404)
    


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
            "password": "admin",
            "email_verified": True,
            "phone_verified": True
        }
        user = User.objects.create_superuser(**data)
        role= Role.objects.get(name__iexact="Aquiline Admin")
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
def get_incident_nature(request):
    incident_natures = IncidentNature.objects.all()
    serialzier = IncidentNatureSerializer(incident_natures, many=True)

    return api_response("Incident Natures fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_threat_level(request):
    threat_levels = ThreatLevel.objects.all()
    serialzier = ThreatLevelSerializer(threat_levels, many=True)

    return api_response("Threat Levels fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_advisory(request):
    advisories = Advisory.objects.all()
    serialzier = AdvisorySerializer(advisories, many=True)

    return api_response("Advisories fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_impact(request):
    impacts = Impact.objects.all()
    serialzier = ImpactSerializer(impacts, many=True)

    return api_response("Advisories fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_primary_threat_actors(request):
    primary_threat_actors = PrimaryThreatActor.objects.all()
    serialzier = PrimaryThreatActorSerializer(primary_threat_actors, many=True)

    return api_response("Advisories fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_alert_type(request):
    alert_types = AlertType.objects.all()
    serialzier = AlertTypeSerializer(alert_types, many=True)

    return api_response("Advisories fetched", serialzier.data, True, 200)

@api_view(["GET"])
def get_affected_group(request):
    affected_groups = AffectedGroup.objects.all()
    serialzier = AffectedGroupSerializer(affected_groups, many=True)

    return api_response("Groups fetched", serialzier.data, True, 200)