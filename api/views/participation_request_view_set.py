from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from api.models.participation_request import ParticipationRequest
from api.serializers.participation_request_serializer import ParticipationRequestSerializer,\
    ExpandedParticipationRequestSerializer


class ParticipationRequestViewSet(mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to request participation in a workout
    and workout owners to allow participation.
    """
    serializer_class = ParticipationRequestSerializer
    filterset_fields = ['workout']

    def update(self, request, *args, **kwargs):
        if 'partial' not in kwargs or not kwargs['partial']:
            raise exceptions.MethodNotAllowed(method='PUT')
        else:
            return super().update(request, *args, **kwargs)

    def _remove_disallowed_fields(self, request):
        if self.action == 'create':
            disallowed_fields = {'status', 'seen'}
        elif self.action == 'partial_update':
            disallowed_fields = {'user', 'workout', 'seen'}
        else:
            disallowed_fields = {}

        for field in disallowed_fields:
            if field in request.data:
                del request.data[field]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        request = None
        if 'request' in context:
            request = context['request']
        if not (request and request.data and request.user):
            return context

        request.data['user'] = request.user.id
        self._remove_disallowed_fields(request)

        return context

    def get_queryset(self):
        if self.action == 'create':
            return ParticipationRequest.objects.filter(user__id=self.request.user.id)
        else:
            return ParticipationRequest.objects.filter(workout__user__id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return ParticipationRequestSerializer
        else:
            return ExpandedParticipationRequestSerializer


participation_request = {
    'id': 1,
    'workout': 1,
    'user': {
        'id': 1,
        'username': 'user97',
    },
    'message': 'bardzo chcialbym biegac tak jak wy'
}


class MockParticipationRequestViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to request participation in a workout.
    """
    permission_classes = [AllowAny]

    def list(self, request):
        return Response([participation_request])

    def create(self, request):
        return Response(participation_request)

    def partial_update(self, request, pk=None):
        accepted_request = dict(participation_request)
        accepted_request['accepted'] = True
        return Response(accepted_request)
