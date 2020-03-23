from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from api.models.participation_request import ParticipationRequest
from api.serializers.participation_request_serializer import ParticipationRequestSerializer


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
        raise exceptions.MethodNotAllowed(method='PUT')

    # TODO can change status only once
    def partial_update(self, request, pk=None):
        if 'user' in request.data:
            del request.data['user']
        if 'workout' in request.data:
            del request.data['workout']
        return super().update(request, partial=True)

    def create(self, request):
        request.data['user'] = request.user.id
        if 'status' in request.data:
            del request.data['status']
        if 'seen' in request.data:
            del request.data['seen']
        return super().create(request)

    def get_queryset(self):
        return ParticipationRequest.objects.filter(user__id=self.request.user.id)


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
