from config.test_setup import TestSetUp
from django.urls import reverse

 
class TestAccountViews(TestSetUp):

    def setUp(self) -> None:
        super().setUp()

    def test_customer_cannot_register_with_no_data(self):
        customer_regitration_url = reverse("customer_signup")
        response = self.client.post(customer_regitration_url)

        self.assertEqual(response.status_code, 400)

    def test_company_cannot_register_with_no_data(self):
        company_regitration_url = reverse("company_signup")
        response = self.client.post(company_regitration_url)

        self.assertEqual(response.status_code, 400)

    def test_customer_can_register_with_correct_data(self):
        customer_data = {
            "email": self.customer_email,
            "first_name": self.customer_firstname,
            "last_name": self.customer_lastname,
            "password": self.password,
            "state": self.state,
            "city": self.city,
            "lga": self.lga,
        }
        customer_regitration_url = reverse("customer_signup")
        response = self.client.post(customer_regitration_url, customer_data)

        self.assertEqual(response.status_code, 201)

    def test_company_can_register_with_correct_data(self):
        company_data = {
            "email": self.company_email,
            "first_name": self.company_firstname,
            "last_name": self.company_lastname,
            "password": self.password,
            "state": self.state,
            "city": self.city,
            "lga": self.lga,
        }
        company_regitration_url = reverse("company_signup")
        response = self.client.post(company_regitration_url, company_data)

        self.assertEqual(response.status_code, 201)
    
    def test_customer_cannot_add_user(self):
        user_data = {
            "email": self.fake.email(),
            "company": self.company_profile.id
        }

        add_user_url = reverse("add_user")
        self.client.force_authenticate(user=self.customer)

        response = self.client.post(add_user_url, data=user_data)
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, 403)
    
    def test_company_can_add_user(self):
        user_data = {
            "email": self.fake.email(),
            "company": self.company_profile.id
        }

        add_user_url = reverse("add_user")
        self.client.force_authenticate(user=self.company)

        response = self.client.post(add_user_url, data=user_data)
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, 201)