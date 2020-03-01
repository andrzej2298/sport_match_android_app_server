from rest_framework.test import APITestCase
from rest_framework import status
from .models.workout import Workout 
from .models.user import User 
from .models.sport import Sport 
from .models.usersport import UserSport

john = {
    'login': 'John',
    'birth_date': '2020-02-06',
    'gender': 'M',
    'email': 'john@example.com'
}

football = {
    'name': 'football'
}

johns_football = {
    'level': 9,
    'user': 1,
    'sport': 1
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
    'level': 9,
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 1,
    'sport': 1
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
    'level': 9,
    'start': '2020-10-10T01:01:00Z',
    'end': '2020-10-10T01:01:00Z',
    'user': 1,
    'sport': 1
}

BASE_URL = 'http://testserver/api/'

class WorkoutTest(APITestCase):
    def setUp(self) -> None:
        self.user = self.add_user(john)
        self.sport = self.add_sport(football)
        user_sport = dict(johns_football)
        user_sport['user'] = self.user
        user_sport['sport'] = self.sport
        self.user_sport = self.add_user_sport(user_sport)
        workout_a = dict(mim_workout)
        workout_b = dict(bitwy_warszawskiej_workout)
        workout_a['user'] = self.user
        workout_b['user'] = self.user
        workout_a['sport'] = self.sport
        workout_b['sport'] = self.sport
        self.workout_a = self.add_workout(workout_a)
        self.workout_b = self.add_workout(workout_b)

    def add_sport(self, item) -> int:
        return self.add_row(item, '/api/sports/')

    def add_user(self, item) -> int:
        return self.add_row(item, '/api/users/')

    def add_workout(self, item) -> int:
        return self.add_row(item, '/api/workouts/')
    
    def add_user_sport(self, item) -> int:
        return self.add_row(item, '/api/user_sports/')

    def add_row(self, item, url) -> int:
        response = self.client.post(url, item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

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
