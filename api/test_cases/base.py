"""
Abstract test case class that implements useful methods used in real test cases.
"""

from rest_framework.test import APITestCase
from rest_framework import status

from .data import *


class TestBase(APITestCase):
    def create_user(self):
        self.user = self.register_user(JOHN)

    def authenticate_user(self):
        token = self.get_token(JOHNS_CREDENTIALS)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def reset_authentication(self):
        self.client.credentials()

    def add_sport(self, sport, success=True) -> int:
        return self.add_row(sport, '/api/sports/', success)

    def register_user(self, user, success=True) -> int:
        return self.add_row(user, '/api/register/', success)

    def add_workout(self, workout, success=True) -> int:
        return self.add_row(workout, '/api/hosted_workouts/', success)

    def add_user_sport(self, user_sport, success=True) -> int:
        return self.add_row(user_sport, '/api/user_sports/', success)

    def get_token(self, user_credentials, success=True) -> str:
        response = self.client.post('/api/login/', user_credentials, format='json')
        self.check(response.status_code, status.HTTP_200_OK, success)
        if success:
            return response.data['token']

    def check(self, status_code, expected_code, success):
        if success:
            self.assertEqual(status_code, expected_code)
        else:
            self.assertNotEqual(status_code, expected_code)

    def add_row(self, item, url, success) -> int:
        response = self.client.post(url, item, format='json')
        self.check(response.status_code, status.HTTP_201_CREATED, success)

        if success:
            return response.data['id']

