
import json
from rest_framework.decorators import api_view
import requests

from accounts_profile.models import Industry, Lga, State
from utils.utils import api_response



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
                    else:
                        continue
            else:
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
        else:
            continue
    return api_response("Industry Populated", {}, True, 200)