from rest_framework.test import APITestCase
from rest_framework import status
from .models import Workout, User, Sport, UserSport

john = {
    'login': 'John',
    'birth_date': '2020-02-06',
    'sex': 'M'
}

football = {
    'name': 'football'
}

johns_football = {
    'level': 9,
    'user': 'http://testserver/api/users/1/',
    'sport': 'http://testserver/api/sports/1/'
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
    'user': 'http://testserver/api/users/1/',
    'sport': 'http://testserver/api/sports/1/'
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
    'user': 'http://testserver/api/users/1/',
    'sport': 'http://testserver/api/sports/1/'
}


class WorkoutTest(APITestCase):
    def setUp(self) -> None:
        self.user = self.add_row(john, '/api/users/')
        self.sport = self.add_row(football, '/api/sports/')
        user_sport = dict(johns_football)
        user_sport['user'] = self.user
        user_sport['sport'] = self.sport
        self.user_sport = self.add_row(user_sport, '/api/user_sports/')
        workout_a = dict(mim_workout)
        workout_b = dict(bitwy_warszawskiej_workout)
        workout_a['user'] = self.user
        workout_b['user'] = self.user
        workout_a['sport'] = self.sport
        workout_b['sport'] = self.sport
        self.workout_a = self.add_row(
            workout_a,
            '/api/workouts/',
        )
        self.workout_b = self.add_row(
            workout_b,
            '/api/workouts/',
        )

    def add_row(self, item, url) -> str:
        response = self.client.post(url, item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['url']

    def test_closest_workouts(self) -> None:
        mim_lat = mim_coordinates[0]
        mim_lon = mim_coordinates[1]
        response = self.client.get(
            f'/api/matching_workouts/?lat={mim_lat}&lon={mim_lon}',
            format='json'
        )
        self.assertEqual(response.data[0]['location']['coordinates'], mim_coordinates)
        self.assertEqual(response.data[1]['location']['coordinates'], bitwy_warszawskiej_coordinates)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dummy(self):
        self.assertTrue(True)
