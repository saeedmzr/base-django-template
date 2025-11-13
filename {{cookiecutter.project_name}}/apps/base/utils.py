from __future__ import annotations

from typing import Any, Callable, Optional, IO
import os

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

User = get_user_model()


class TestHelper:
    """
    Utilities for authenticating test clients with JWT, assigning headers, injecting sessions,
    and asserting common response shapes. Works with JSON-only DRF configuration.
    """

    # Namespace-aware endpoints (adjust if your URL names differ)
    LOGIN_URL_NAME = "api:users:login"

    # ---- Authentication ----
    @staticmethod
    def get_access_for_user(user: User) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def authenticate_client(client: APIClient, user: User | int | str) -> str:
        """
        Accepts User instance, user id, or username; sets Bearer token on client.
        Returns the access token string.
        """
        if isinstance(user, User):
            u = user
        elif isinstance(user, int):
            u = User.objects.get(id=user)
        else:
            u = User.objects.get(username=user)
        token = TestHelper.get_access_for_user(u)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return token

    @staticmethod
    def login_and_authenticate(client: APIClient, username: str, password: str) -> str:
        """
        Hits the login endpoint and sets returned access token on the client.
        Requires that your TokenObtainPairView is mounted at api:users:login.
        """
        login_url = reverse(TestHelper.LOGIN_URL_NAME)
        resp = client.post(login_url, {"username": username, "password": password}, format="json")
        assert resp.status_code == status.HTTP_200_OK, f"Login failed: {resp.status_code} {resp.data}"
        token = resp.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return token

    @staticmethod
    def attach_session(client: APIClient, session_data: dict[str, Any]) -> None:
        """
        Attach/modify session for the APIClient. Useful for org scoping etc.
        """
        session = client.session
        for k, v in session_data.items():
            session[k] = v
        session.save()

    @staticmethod
    def build_request_with_session() -> tuple[Any, SessionMiddleware]:
        """
        Build a bare request and add a Session via middleware for low-level view tests.
        """
        factory = RequestFactory()
        req = factory.get("/")
        sm = SessionMiddleware(lambda r: r)
        sm.process_request(req)
        req.session.save()
        return req, sm

    # ---- Assertions ----
    @staticmethod
    def assert_ok_json(assertion: Callable, response, expected_data_keys: list[str] | None = None) -> None:
        assertion(response.status_code, status.HTTP_200_OK)
        assert isinstance(response.data, dict), "Response should be a JSON object"
        if expected_data_keys:
            for key in expected_data_keys:
                assert key in response.data, f"Missing key in response.data: {key}"

    @staticmethod
    def assert_status(assertion: Callable, response, expected_http_status: int) -> None:
        assertion(response.status_code, expected_http_status)

    # ---- File helper (context manager) ----
    class open:
        def __init__(self, file: str, mode: str, base_file: str) -> None:
            base_dir = os.path.dirname(os.path.abspath(base_file))
            self.file = open(os.path.join(base_dir, file), mode)

        def __enter__(self) -> IO[bytes | str]:
            return self.file

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            self.file.close()


class RequestsClient:
    """
    A thin wrapper to emulate `requests`-like calls using DRF's APIClient with JSON-only behavior.
    """
    def __init__(self) -> None:
        self.client = APIClient()

    def request(
        self,
        method: str,
        url: str,
        json: Optional[dict[str, Any]],
        timeout: int,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        if headers and "Authorization" in headers:
            self.client.credentials(HTTP_AUTHORIZATION=headers["Authorization"])
        else:
            self.client.credentials()  # clear
        call = getattr(self.client, method.lower())
        return call(path=url, data=json, format="json")

    def mount(self, *args, **kwargs):
        return
