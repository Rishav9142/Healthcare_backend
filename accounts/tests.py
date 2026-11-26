from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationApiTests(APITestCase):
    register_url = "/api/auth/register/"
    login_url = "/api/auth/login/"

    def test_registration_creates_user_with_hashed_password(self):
        response = self.client.post(
            self.register_url,
            {
                "name": "Alex Patient",
                "email": "ALEX@example.com",
                "password": "StrongPass!492",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "alex@example.com")
        self.assertNotIn("password", response.data)

        user = User.objects.get(email="alex@example.com")
        self.assertTrue(user.check_password("StrongPass!492"))

    def test_registration_rejects_duplicate_email_and_weak_password(self):
        User.objects.create_user(
            email="alex@example.com",
            name="Alex Patient",
            password="StrongPass!492",
        )

        duplicate_response = self.client.post(
            self.register_url,
            {
                "name": "Another Alex",
                "email": "ALEX@example.com",
                "password": "OtherStrong!492",
            },
            format="json",
        )
        weak_password_response = self.client.post(
            self.register_url,
            {
                "name": "New Patient",
                "email": "new@example.com",
                "password": "password",
            },
            format="json",
        )

        self.assertEqual(
            duplicate_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("email", duplicate_response.data)
        self.assertEqual(
            weak_password_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("password", weak_password_response.data)

    def test_login_returns_jwt_pair_for_valid_credentials(self):
        User.objects.create_user(
            email="alex@example.com",
            name="Alex Patient",
            password="StrongPass!492",
        )

        response = self.client.post(
            self.login_url,
            {"email": "alex@example.com", "password": "StrongPass!492"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {"email": "unknown@example.com", "password": "WrongPassword!492"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
