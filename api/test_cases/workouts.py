from rest_framework import status

from .base import TestBase
from .data import *


class WorkoutTest(TestBase):
    def test_workout_creation(self):
        self.create_user()
        self.authenticate_user()

        self.sport = JOHNS_RUNNING['sport']
        self.user_sport = self.add_user_sport(JOHNS_RUNNING)
        workout_a = dict(MIM_WORKOUT)
        workout_b = dict(BITWY_WARSZAWSKIEJ_WORKOUT)
        workout_a['sport'] = self.sport
        workout_b['sport'] = self.sport
        self.workout_a = self.add_workout(workout_a)
        self.workout_b = self.add_workout(workout_b)
