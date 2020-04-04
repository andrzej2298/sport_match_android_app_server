from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from api.models.workout import Workout
from api.serializers.workout_serializer import WorkoutSerializer
from api.views.paginators import ResultPagination


class SuggestedWorkoutViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint that allows workout suggestions to be viewed.
    """
    serializer_class = WorkoutSerializer
    filterset_fields = ['sport']
    pagination_class = ResultPagination

    def get_queryset(self):
        return Workout.objects.exclude(user__id=self.request.user.id)


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