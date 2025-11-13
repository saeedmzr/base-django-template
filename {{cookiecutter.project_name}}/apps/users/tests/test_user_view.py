# apps/users/tests/test_user_view.py
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from apps.base.utils import TestHelper
from apps.users.enums import UserRoleEnum

User = get_user_model()


class UserViewSetTest(APITestCase):
    fixtures = ["users.json"]

    def setUp(self):
        # Endpoints (namespaced)
        self.login_url = reverse(TestHelper.LOGIN_URL_NAME)
        self.list_url = reverse("api:users:user-list")

        # If fixtures are loaded, fetch seeded users by username
        self.admin = User.objects.get(username="adminuser")
        self.editor = User.objects.get(username="editoruser")
        self.viewer = User.objects.get(username="vieweruser")

    def auth(self, username: str, password: str = "1234"):
        TestHelper.login_and_authenticate(self.client, username, password)

    def test_list_requires_viewer_plus(self):
        # Unauthenticated -> 401
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Viewer -> 200 and payload shape
        self.auth("vieweruser")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("users", resp.data["data"])
        self.client.credentials()

        # Editor -> 200
        self.auth("editoruser")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # Admin -> 200
        self.auth("adminuser")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_requires_viewer_plus(self):
        # Target user to retrieve
        target = self.viewer
        detail_url = reverse("api:users:user-detail", args=[target.id])

        # Unauthenticated -> 401
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Viewer -> 200
        self.auth("vieweruser")
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("user", resp.data["data"])
        self.client.credentials()

        # Editor -> 200
        self.auth("editoruser")
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # Admin -> 200
        self.auth("adminuser")
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_me_returns_current_user(self):
        # default url_name from method get_me => 'get-me' -> reverse name 'api:user-get-me'
        me_url = reverse("api:users:user-get-me")

        # Unauthenticated -> 401
        resp = self.client.get(me_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated viewer -> 200 with current user data
        self.auth("vieweruser")
        resp = self.client.get(me_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("user", resp.data["data"])
        self.assertEqual(resp.data["data"]["user"]["id"], self.viewer.id)

    def test_create_requires_admin(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "role": UserRoleEnum.VIEWER.value,
            "password": "Testpass123!",
            "confirm_password": "Testpass123!",
        }

        # Unauthenticated -> 401
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Viewer -> 403
        self.auth("vieweruser")
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        # Editor -> 403
        self.auth("editoruser")
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        # Admin -> 201 and response includes user
        self.auth("adminuser")
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", resp.data["data"])

    def test_update_requires_editor_plus(self):
        target = self.viewer
        detail_url = reverse("api:users:user-detail", args=[target.id])
        payload = {"email": "viewer.updated@example.com"}

        # Unauthenticated -> 401
        resp = self.client.put(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Viewer -> 403
        self.auth("vieweruser")
        resp = self.client.put(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        # Editor -> 200
        self.auth("editoruser")
        resp = self.client.put(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("user", resp.data["data"])
        self.client.credentials()

        # Admin -> 200
        self.auth("adminuser")
        resp = self.client.put(detail_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_destroy_requires_admin(self):
        target = self.editor
        detail_url = reverse("api:users:user-detail", args=[target.id])

        # Unauthenticated -> 401
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Viewer -> 403
        self.auth("vieweruser")
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        # Editor -> 403
        self.auth("editoruser")
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        # Admin -> 200
        self.auth("adminuser")
        resp = self.client.delete(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
