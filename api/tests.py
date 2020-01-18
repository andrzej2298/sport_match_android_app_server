from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Workout, User, Sport, UserSport

john = {
    "login": "John",
    "birth_date": "2020-02-06",
    "sex": "M"
}

football = {
    'name': 'football'
}

johns_football = {
    'proficiency': 9,
    'user': 'http://localhost:8000/api/users/1/',
    'sport': 'http://localhost:8000/api/sports/1/'
}

mim_coordinates = [
    52.211769,
    20.982064
]
mim_workout = {
    'name': 'MIM',
    'location': {
        'type': 'Point',
        'coordinates': mim_coordinates,
    },
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 'http://localhost:8000/api/users/1/',
    'sport': 'http://localhost:8000/api/sports/1/'
}

bitwy_warszawskiej_coordinates = [
    52.211858,
    20.977279
]
bitwy_warszawskiej_workout = {
    'name': 'Bitwy Warszawskiej',
    'location': {
        'type': 'Point',
        'coordinates': bitwy_warszawskiej_coordinates,
    },
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 'http://localhost:8000/api/users/1/',
    'sport': 'http://localhost:8000/api/sports/1/'
}


class WorkoutTest(APITestCase):
    def setUp(self) -> None:
        self.add_row(john, '/api/users/', User)
        self.add_row(football, '/api/sports/', Sport)
        self.add_row(johns_football, '/api/user_sports/', UserSport)
        self.add_row(
            mim_workout,
            '/api/workouts/',
            Workout,
            expected_count=1,
        )
        self.add_row(
            bitwy_warszawskiej_workout,
            '/api/workouts/',
            Workout,
            expected_count=2,
        )

    def add_row(self, user, url, instance_class, expected_count=1):
        response = self.client.post(url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(instance_class.objects.count(), expected_count)

    def test_closest_workouts(self):
        mim_lat = mim_coordinates[0]
        mim_lon = mim_coordinates[1]
        response = self.client.get(
            f'/api/matching_workouts/?lat={mim_lat}&lon={mim_lon}',
            format='json'
        )
        self.assertEqual(response.data[0]['location']['coordinates'], mim_coordinates)
        self.assertEqual(response.data[1]['location']['coordinates'], bitwy_warszawskiej_coordinates)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
