from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from api.models.workout import Workout
from api.serializers.workoutserializer import WorkoutSerializer, WorkoutSerializerExpanded


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows workouts to be viewed or edited.
    """
    queryset = Workout.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return WorkoutSerializerExpanded
        else:
            return WorkoutSerializer


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
            serializer = WorkoutSerializer(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        else:
            serializer = WorkoutSerializer(Workout.objects.all(), context={'request': request}, many=True)
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

    def list(self, request):
        return Response([workout_info])

    def retrieve(self, request, pk=None):
        full_info = dict(workout_info)
        full_info['author'] = {
                                  'id': 2,
                                  'name': 'John',
                              },
        full_info['user_list'] = [
            {
                'id': 78943107,
                'login': 'Kot',
            },
            {
                'id': 5411259,
                'login': 'Pies',
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
