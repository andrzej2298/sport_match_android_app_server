from rest_framework import viewsets
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