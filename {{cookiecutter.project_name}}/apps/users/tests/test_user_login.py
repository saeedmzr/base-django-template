from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from apps.users.models import User
from apps.users.enums import UserRoleEnum


class UserLoginTest(APITestCase):

    def setUp(self):
        self.login_url = reverse("api:users:login")

    def create_user(self, username, email, role, password='Testpass123!'):
        """
        Helper to create user with given role
        """
        return User.objects.create_user(
            username=username,
            email=email,
            role=role,
            password=password
        )

    def test_admin_user_login(self):
        user = self.create_user('adminuser', 'admin@example.com', UserRoleEnum.ADMIN.value)
        response = self.client.post(self.login_url, {'username': 'adminuser', 'password': 'Testpass123!'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_editor_user_login(self):
        user = self.create_user('editoruser', 'editor@example.com', UserRoleEnum.EDITOR.value)
        response = self.client.post(self.login_url, {'username': 'editoruser', 'password': 'Testpass123!'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_viewer_user_login(self):
        user = self.create_user('vieweruser', 'viewer@example.com', UserRoleEnum.VIEWER.value)
        response = self.client.post(self.login_url, {'username': 'vieweruser', 'password': 'Testpass123!'},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_wrong_password(self):
        user = self.create_user('testuser', 'test@example.com', UserRoleEnum.VIEWER.value)
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'WrongPassword!'},format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
