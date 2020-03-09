from rest_framework import viewsets
from rest_framework.response import Response


class MockLoginViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to log in.
    """
    def create(self, request):
        return Response({
            'token': '123456789123456789',
        })
