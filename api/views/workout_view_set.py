import logging
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django_filters.rest_framework import FilterSet, IsoDateTimeFromToRangeFilter
from api.models.workout import Workout
from api.models.participation_request import ParticipationRequest
from api.serializers.workout_serializer import FullWorkoutSerializer
from api.models.constants import PENDING, ACCEPTED, REJECTED


class HostedWorkoutViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    API endpoint that allows workouts hosted by user to be viewed or edited.
    """
    serializer_class = FullWorkoutSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        response = super().create(request, *args, **kwargs)

        if response.status_code == HTTP_201_CREATED:
            logging.getLogger('ai_model').info(f'WORKOUT {response.data["id"]} CREATED')

        return response

    def get_queryset(self):
        return Workout.objects.filter(user__id=self.request.user.id)


def get_request_related_workouts(**kwargs):
    workouts = {
        request.workout for request in
        ParticipationRequest.objects.filter(**kwargs).select_related('workout')
    }
    return workouts


class PendingWorkoutViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    API endpoint that allows workouts pending approval to be viewed or edited.
    """
    serializer_class = FullWorkoutSerializer

    def get_queryset(self):
        return get_request_related_workouts(user__id=self.request.user.id, status=PENDING)


class RecentlyAcceptedWorkoutViewSet(mixins.ListModelMixin,
                                     viewsets.GenericViewSet):
    """
    API endpoint that allows recently accepted workouts to be viewed or edited.
    """
    serializer_class = FullWorkoutSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        relevant_requests = ParticipationRequest.objects.filter(user__id=user_id, status=ACCEPTED, seen=False)
        recently_accepted = {
            request.workout for request in relevant_requests.select_related('workout')
        }

        relevant_requests.update(seen=True)

        return recently_accepted


class RecentlyRejectedWorkoutViewSet(mixins.ListModelMixin,
                                     viewsets.GenericViewSet):
    """
    API endpoint that allows recently rejected workouts to be viewed or edited.
    """
    serializer_class = FullWorkoutSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        relevant_requests = ParticipationRequest.objects.filter(user__id=user_id, status=REJECTED, seen=False)
        recently_accepted = {
            request.workout for request in relevant_requests.select_related('workout')
        }
        relevant_requests.update(seen=True)

        return recently_accepted


class DateFilter(FilterSet):
    start_time = IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Workout
        fields = ['start_time']


class WorkoutViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint that allows specific workouts to be viewed or edited.
    Filtering by date and time is allowed.
    """
    filter_class = DateFilter

    def get_queryset(self):
        if self.action == 'list':
            user_id = self.request.user.id
            hosted = Workout.objects.filter(user__id=user_id)

            accepted_requests = [
                request.workout.id
                for request in ParticipationRequest.objects.filter(user__id=user_id, status=ACCEPTED)
            ]
            # filtering after union is not allowed, so filter_queryset has to be applied here
            taking_part_in = Workout.objects.filter(id__in=accepted_requests)

            return hosted | taking_part_in
        elif self.action == 'retrieve':
            return Workout.objects.all()

    def get_serializer_class(self):
        # TODO permissions
        return FullWorkoutSerializer


class MatchingWorkoutViewSet(viewsets.ViewSet):
    """
    API endpoint that allows matching workouts to be viewed.
    """

    def list(self, request):
        if 'lat' in request.query_params and 'lon' in request.query_params:
            reference_point = Point(
                float(request.query_params['lat']),
                float(request.query_params['lon']),
            )
            queryset = Workout.objects.filter(
                location__distance_lte=(reference_point, D(km=10))
            ).annotate(
                distance=Distance('location', reference_point)
            ).order_by('distance')
            serializer = FullWorkoutSerializer(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        else:
            serializer = FullWorkoutSerializer(Workout.objects.all(), context={'request': request}, many=True)
            return Response(serializer.data)


workout_info = {
    'id': 1,
    'name': 'Biegamy 2013',
    'max_people': 334,
    'signed_people': 333,
    'sport': 3,
    'desired_proficiency': 1,
    'location': {
        'type': 'Point',
        "coordinates": [
            0.0,
            0.0
        ]
    },
    'location_name': 'Warszawa',
    'start_time': '',
    'end_time': '',
    'description': '',
    'age_min': 0,
    'age_max': 90,
    'expected_gender': 'F',
}

basic_workout_info = {
    'id': 1,
    'name': 'Biegamy 2013',
    'location_name': 'Warszawa',
}

workout_suggestions = {
    'count': 30,
    'next': '/workouts/suggested/?page=2',
    'results': [
        {
            'id': 1,
            'name': 123,
            'author': {'id': 1, 'name': 'Szymon'},
            'location_name': 'Polska',
            'location': {
                'type': 'Point',
                "coordinates": [
                    0.0,
                    0.0
                ]
            },
        }
    ]
}


class MockWorkoutViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to view and update the workouts they are participating in.
    """
    permission_classes = [AllowAny]

    def list(self, request):
        return Response([workout_info])

    def retrieve(self, request, pk=None):
        full_info = dict(workout_info)
        full_info['author'] = {
            'id': 2,
            'name': 'John',
        }
        full_info['user_list'] = [
            {
                'id': 78943107,
                'username': 'Kot',
            },
            {
                'id': 5411259,
                'username': 'Pies',
            },
        ]
        return Response(full_info)

    def create(self, request):
        return Response(workout_info)

    def update(self, request, pk=None):
        return Response(workout_info)

    def partial_update(self, request, pk=None):
        return Response(workout_info)

    @action(methods=['get'], detail=False)
    def recently_accepted(self, request):
        return Response([basic_workout_info])

    @action(methods=['get'], detail=False)
    def recently_rejected(self, request):
        return Response([basic_workout_info])

    @action(methods=['get'], detail=False)
    def pending(self, request):
        return Response([workout_info])

    @action(methods=['get'], detail=False)
    def hosted(self, request):
        return Response([workout_info])

    @action(methods=['get'], detail=False)
    def suggested(self, request):
        return Response(workout_suggestions)
