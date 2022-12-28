from http import client
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from accounts.serializers import GoogleAuthSerializer
from decouple import config


def get_user_data(credential: str, platform: str):
    client_id = config("GOOGLE_CLIENT_ID")
    user_data = id_token.verify_oauth2_token(
        credential,
        google_requests.Request(),
        client_id,
    )
    return user_data
