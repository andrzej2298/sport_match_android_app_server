from rest_framework import status

from .base import TestBase
from .data import *


class WorkoutTest(TestBase):
    def setUp(self) -> None:
        self.create_user()
        self.authenticate_user()

        self.sport = self.add_sport(FOOTBALL)
        user_sport = dict(JOHNS_FOOTBALL)
        user_sport['user'] = self.user
        user_sport['sport'] = self.sport
        self.user_sport = self.add_user_sport(user_sport)
        workout_a = dict(MIM_WORKOUT)
        workout_b = dict(BITWY_WARSZAWSKIEJ_WORKOUT)
        workout_a['user'] = self.user
        workout_b['user'] = self.user
        workout_a['sport'] = self.sport
        workout_b['sport'] = self.sport
        self.workout_a = self.add_workout(workout_a)
        self.workout_b = self.add_workout(workout_b)

    def test_closest_workouts(self) -> None:
        mim_lat = MIM_COORDINATES[0]
        mim_lon = MIM_COORDINATES[1]
        response = self.client.get(
            f'/api/matching_workouts/?lat={mim_lat}&lon={mim_lon}',
            format='json'
        )
        self.assertEqual(response.data[0]['location']['coordinates'], MIM_COORDINATES)
        self.assertEqual(response.data[1]['location']['coordinates'], BITWY_WARSZAWSKIEJ_COORDINATES)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dummy(self):
        self.assertTrue(True)
