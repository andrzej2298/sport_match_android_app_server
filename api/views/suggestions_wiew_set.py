from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from api.models.workout import Workout
from api.serializers.workout_serializer import WorkoutSerializer
from ..paginators import ResultPagination


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
