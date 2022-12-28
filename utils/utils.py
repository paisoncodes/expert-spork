from random import randint
from rest_framework.response import Response
from rest_framework import status as status_code
import json


def random_with_n_digits(n=12):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)

def api_response(message:str, data:json, status:bool, code:int)->Response:
    response = {
        "message": message,
        "data": data,
        "status": status,
    }
    if code == 200:
        return Response(response, status=status_code.HTTP_200_OK)
    elif code == 201:
        return Response(response, status=status_code.HTTP_201_CREATED)
    elif code == 202:
        return Response(response, status=status_code.HTTP_202_ACCEPTED)
    elif code == 400:
        return Response(response, status=status_code.HTTP_400_BAD_REQUEST)
    elif code == 401:
        return Response(response, status=status_code.HTTP_401_UNAUTHORIZED)
    else:
        return Response(response, status=status_code.HTTP_500_INTERNAL_SERVER_ERROR)