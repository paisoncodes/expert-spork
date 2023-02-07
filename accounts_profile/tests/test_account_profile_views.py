from config.test_setup import TestSetUp
from django.urls import reverse

class TestAccountProfileViews(TestSetUp):

    def setUp(self) -> None:
        super().setUp()

    def test_update_user_profile(self):
        user_profile_url = reverse("user_profile")
        update_data = {
            "first_name": self.fake.name().title()
        }
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(user_profile_url, data=update_data)
        self.client.force_authenticate(user=None)

        assert response.status_code == 200

    def test_update_company_profile(self):
        user_profile_url = reverse("company_profile")
        update_data = {
            "company_name": self.fake.word().title()
        }
        self.client.force_authenticate(user=self.company)
        response = self.client.put(user_profile_url, data=update_data)
        self.client.force_authenticate(user=None)

        assert response.status_code == 200
