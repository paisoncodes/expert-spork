from config.test_setup import TestSetUp
from django.urls import reverse
import random

from datetime import date, time


class TestIncidentViews(TestSetUp):

    def setUp(self) -> None:
        super().setUp()
    
    def test_user_can_view_all_incidents_they_created(self):
        self.client.force_authenticate(user=self.customer)
        request_url = reverse("incidents")

        response = self.client.get(request_url)
        self.client.force_authenticate(user=None)

        assert response.status_code == 200

    def test_user_can_view_all_incidents(self):
        self.client.force_authenticate(user=self.customer)
        request_url = reverse("all_incidents")

        response = self.client.get(request_url)
        self.client.force_authenticate(user=None)

        assert response.status_code == 200
    
    def test_users_can_create_incident(self):
        self.client.force_authenticate(user=self.customer)
        request_url = reverse("incidents")

        incident_data = {
            "name": self.fake.word().title(),
            "incident_type": self.fake.word().title(),
            "owner": random.choice([self.customer.id, self.company.id]),
            "date": self.fake.date(),
            "time": self.fake.time(),
            "details": self.fake.text(),
            "location": self.fake.address(),
            "special_events": self.fake.sentence(),
            "prior_warnings": self.fake.sentence(),
            "perpetrators": self.fake.sentence(),
            "nature_of_incident": self.fake.sentence()
        }

        response = self.client.post(request_url, data=incident_data)
        self.client.force_authenticate(user=None)

        assert response.status_code == 201
