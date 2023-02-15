
import json
from rest_framework.decorators import api_view
import requests

from accounts_profile.models import Lga, State
from utils.utils import api_response



@api_view(["GET"])
def populate_state(request):
    try:
        url_1 = "https://api.facts.ng/v1/states/"
        response = requests.request("GET", url_1)
        print(response.json())
        for state in response.json():
            state_ = State.objects.create(state=state["name"])
            lgas = (requests.request("GET", state["uri"])).json()
            for lga in lgas["lgas"]:
                Lga.objects.create(lga=lga, state=state_)
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