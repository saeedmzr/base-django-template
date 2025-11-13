from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from apps.base.utils import TestHelper

User = get_user_model()

class UserFlowTests(APITestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.list_url = reverse("api:users:user-list")
        self.me_url = reverse("api:users:user-get-me")
        self.login_url = reverse(TestHelper.LOGIN_URL_NAME)

    def test_viewer_can_list(self):
        TestHelper.login_and_authenticate(self.client, "vieweruser", "1234")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_admin_can_create(self):
        TestHelper.login_and_authenticate(self.client, "adminuser", "1234")
        resp = self.client.post(self.list_url, {
            "username": "newuser",
            "email": "new@example.com",
            "role": "viewer",
            "password": "Testpass123!",
            "confirm_password": "Testpass123!",
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
