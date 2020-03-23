from rest_framework import mixins, viewsets
from api.models.workout import Workout
from api.serializers.workout_serializer import WorkoutSerializer


class SuggestedWorkoutViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint that allows workout suggestions to be viewed.
    """
    serializer_class = WorkoutSerializer
    filterset_fields = ['sport']

    def get_queryset(self):
        return Workout.objects.exclude(user__id=self.request.user.id)
