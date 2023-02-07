from typing import Any
from rest_framework.test import APITestCase
from django.urls import reverse
from mixer.backend.django import mixer
from faker import Faker
from faker.providers.phone_number import Provider

from accounts.models import User
from accounts_profile.models import CompanyProfile
from rest_framework.authtoken.models import Token
from rest_framework import response
import random

from incident.models import Incident


class PhoneNumberProvider(Provider):
    def nigerian_phone_number(self) -> str:
        return f"+234 {self.msisdn()[3:]}"

class TestSetUp(APITestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.fake.add_provider(PhoneNumberProvider)
        self.customer_email = self.fake.email()
        self.company_email = self.fake.email()
        self.customer_firstname= self.fake.first_name().title()
        self.customer_lastname= self.fake.last_name().title()
        self.customer_phone= self.fake.nigerian_phone_number()
        self.company_firstname= self.fake.first_name().title()
        self.company_lastname= self.fake.last_name().title()
        self.company_phone= self.fake.nigerian_phone_number()
        self.customer_username = self.customer_email.split('@')[0]
        self.company_username = self.company_email.split('@')[0]
        self.password = self.fake.password()
        self.state = self.fake.state()
        self.city = self.fake.city()
        self.lga = self.city + " " + self.state
        self.customer = mixer.blend(User, email=self.fake.email(), password=self.fake.password())
        self.company = mixer.blend(User, email=self.fake.email(), user_type=User.UserType.COMPANY, password=self.fake.password())
        self.company_profile = CompanyProfile.objects.get()
        incident_data = {
            "name": self.fake.word().title(),
            "incident_type": self.fake.word().title(),
            "date": self.fake.date(),
            "time": self.fake.time(),
            "details": self.fake.text(),
            "location": self.fake.address(),
            "special_events": self.fake.sentence(),
            "prior_warnings": self.fake.sentence(),
            "perpetrators": self.fake.sentence(),
            "nature_of_incident": self.fake.sentence()
        }
        self.incident = mixer.blend(Incident, **incident_data, owner=random.choice([self.customer, self.company]))
        return super().setUp()
    
    def postTest(self, url, data, require_login=False) -> "response":
        pass

    def getTest(self):
        pass

    def putTest(self):
        pass

    def deleteTest(self):
        pass
    
    def tearDown(self) -> None:
        return super().tearDown()