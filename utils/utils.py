from random import randint
from rest_framework.response import Response
from rest_framework import status as status_code
import json
import requests
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import *

from notifications.models import Messages, Emails, Notification

from subscription.models import EXPIRED, Subscription

from datetime import datetime



def random_with_n_digits(n=12):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)

def validate_phone_number(phone_number:str)->bool:
    if len(phone_number) > 13:
        return False
    if len(phone_number) < 13:
        return False
    if phone_number[:3] != "234":
        return False
    return True

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

def send_message(receiver:str, message:str, user_email:str) -> None:
    url = "https://api.ng.termii.com/api/sms/send"
    payload = {
            "to": receiver,
            "from": "Aquiline Alerts",
            "sms": message,
            "type": "plain",
            "channel": "dnd",
            "api_key": settings.TERMII_API_KEY,
        }
    headers = {
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    response = response.json()
    # TODO: Remove this after fixing the issue with the sms service
    print("yeeeeeeeeeeeeee", response)
    
    Messages.objects.create(
        receiver=receiver,
        message=message,
        sent= True if response["message"] == "Successfully Sent" else False,
        response_message=response["message"],
        message_id=response["message_id"] if response["message"] == "Successfully Sent" else False,
        email = user_email
    )

def generate_password(comapany_name, company_count):
    return f"{comapany_name.title()}.{company_count}"

def send_mail(receiver:str, subject:str, body:str) -> None:
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email("olatunji@gdsplusltd.com")
    to_email = To(receiver)
    subject = subject
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # response = json.loads(response)
    Emails.objects.create(
        receiver=receiver,
        message=body,
        sent= True if response.status_code == 202 else False,
        response_message=response.body if response.status_code == 202 else "",
        status_code=response.status_code,
        email = receiver,
        subject=subject,
    )

def check_subscription_status():
    try:
        subscriptions = Subscription.objects.all().exclude(status=EXPIRED)
        import pytz
        utc=pytz.UTC
        
        for subscription in subscriptions:
            if subscription.expiry_date.replace(tzinfo=utc) <= (datetime.now()).replace(tzinfo=utc):
                subscription.status = EXPIRED
                subscription.save()
                Notification.objects.create(title=f"You reported an incident.", user=subscription.customer, object_id=subscription.id)
                subject = "Subscription Expireed"

                message = "Your subscription has expired."

                send_mail(subscription.customer.email, subject=subject, body=message)
    except Exception as e:
        import logging
        logging.exception(str(e))



