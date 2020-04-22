from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models.functions import Now
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError

import numpy as np

from api.models.constants import SPORTS, MIN_PROFICIENCY_VALUE, MAX_PROFICIENCY_VALUE
from api.models.workout import Workout
from api.models.user import User
from api.models.user_sport import UserSport
from api.models.suggested_workout_history import SuggestedWorkoutHistoryItem, add_suggested_workout_to_history
from api.serializers.workout_serializer import FullWorkoutSerializer, get_people_signed_for_a_workout
from api.serializers.suggestion_request_serializer import SuggestionRequestSerializer
from api.utils.time import get_current_age
from api.views.paginators import ResultPagination


class SuggestedWorkoutViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint that allows workout suggestions to be viewed.
    """
    serializer_class = FullWorkoutSerializer
    filterset_fields = ['sport']
    pagination_class = ResultPagination

    def _initial_workout_filter(self, user, data):
        age = get_current_age(user.birth_date)

        filtered_workouts = (
            Workout.objects
            .exclude(user=user)
            .filter(
                location__distance_lte=(data['location'], D(km=100)),  # user within 100 km of the workout
                start_time__gte=Now(),  # workout hasn't started yet
                age_min__lte=age,  # at least min age
                age_max__gte=age,  # at most max age
            )
            .annotate(distance=Distance('location', data['location']))
        )

        if 'sport' in data and data['sport']:
            filtered_workouts = filtered_workouts.filter(sport=data['sport'])
        return filtered_workouts

    def get_queryset(self):
        request_data = self.request.data
        user = User.objects.get(id=self.request.user.id)

        if not request_data:
            raise ValidationError('must provide at least location')

        serializer = SuggestionRequestSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        filtered_workouts = self._initial_workout_filter(user, data)
        return _get_recommended_workouts(filtered_workouts[:100], user, data)


def _one_hot(i, value_range):
    array = [0 for _ in range(value_range)]
    array[i] = 1
    return array


def _get_user_proficiency(user_sports, workout_sport_id):
    try:
        return user_sports.get(sport=workout_sport_id).level
    except ObjectDoesNotExist:
        return MIN_PROFICIENCY_VALUE


def _get_workout_has_ben_seen(user: User, workout: dict):
    return int(SuggestedWorkoutHistoryItem.objects.filter(user=user, workout=workout['id']).exists())


_POSSIBLE_PROFICIENCY_VALUES = MAX_PROFICIENCY_VALUE - MIN_PROFICIENCY_VALUE + 1
_POSSIBLE_SPORTS = len(SPORTS)


def _generate_workout_values(workouts, user, user_sports, request_data, now):
    for w in workouts.values():
        workout_start_time = w['start_time']
        workout_end_time = w['end_time']
        workout_location = w['location']
        workout_sport_id = w['sport_id']
        distance_to_workout = w['distance']
        user_proficiency = _get_user_proficiency(user_sports, workout_sport_id)
        workout_has_ben_seen = _get_workout_has_ben_seen(user, w)
        user_location = request_data['location']

        yield [
            w['id'],  # workout id
            (workout_start_time - now).seconds / 60,  # minutes to workout
            distance_to_workout.m,  # metres to workout
            workout_location.x,  # workout location x
            workout_location.y,  # workout location y
            user_location.x,  # user location x
            user_location.y,  # user location y
            workout_start_time.hour * 60 + workout_start_time.minute,  # minutes from midnight to start
            workout_end_time.hour * 60 + workout_end_time.minute,  # minutes from midnight to end
            *_one_hot(workout_start_time.weekday(), 7),  # day of the week
            *_one_hot(workout_sport_id - 1, _POSSIBLE_SPORTS),  # sport_id
            *_one_hot(w['desired_proficiency'], _POSSIBLE_PROFICIENCY_VALUES),  # workout sport proficiency
            *_one_hot(user_proficiency, _POSSIBLE_PROFICIENCY_VALUES),  # user's proficiency
            w['age_min'],
            w['age_max'],
            workout_has_ben_seen,
            get_people_signed_for_a_workout(w['id']),  # people taking part in the workout
            w['max_people'],
            1,  # TODO common workouts, mock value for now
        ]


# TODO function which should be replaced with a call to the
#   machine learning model, this function adds a recommendation
#   of value 1 for every workout
def _get_workout_recommendations(array: np.array):
    (rows, columns) = array.shape
    selected_columns = [False for _ in range(columns)]
    selected_columns[0] = True  # workout id
    array = array[:, selected_columns]  # filter only ids

    # append an extra column with dummy recommendations values
    result = np.ones((rows, 2))
    result[:, :-1] = array
    return result


def _get_recommended_workouts(workouts, user, request_data):
    user_sports = UserSport.objects.filter(user=user)
    filtered = np.array(list(_generate_workout_values(workouts, user, user_sports, request_data, timezone.now())))

    # no suggestions, prevent accessing non existent columns
    if filtered.size == 0:
        return Workout.objects.none()

    recommended = _get_workout_recommendations(filtered)

    # sort recommendations by value
    sorted_by_recommendation_value = recommended[recommended[:, 1].argsort()][::-1]
    # convert back to ints (numpy stored ids as floats)
    recommended_ids = {int(workout_id) for workout_id in sorted_by_recommendation_value[:, 0].tolist()}
    # cannot filter the queryset directly, because it already has been sliced before
    recommended_workouts = Workout.objects.filter(id__in=recommended_ids)

    # update recommendation history in the database
    for workout_id in recommended_workouts:
        add_suggested_workout_to_history(workout_id, user)

    return recommended_workouts
