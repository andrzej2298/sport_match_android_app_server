from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import User, Workout, Sport, UserSport

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, WorkoutSerializer
from .serializers import SportSerializer, UserSportSerializer


# def index(request):
#     return JsonResponse({
#         'hello': 'world'
#     })
#
# def users(request):
#     all_users = serialize('json', User.objects.all())
#     return HttpResponse(all_users, content_type='application/json')
#
#
# def workouts(request):
#     all_workouts = serialize('json', Workout.objects.all(), use_natural_foreign_keys=True)
#     return HttpResponse(all_workouts, content_type='application/json')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sports to be viewed or edited.
    """
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

class UserSportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user's sports to be viewed or edited.
    """
    queryset = UserSport.objects.all()
    serializer_class = UserSportSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows workouts to be viewed or edited.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


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
