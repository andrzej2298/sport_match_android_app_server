from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..errors import BAD_USERNAME


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(BAD_USERNAME)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
        })

class MockLoginViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to log in.
    """
    permission_classes = [AllowAny]
    def create(self, request):
        return Response({
            'token': '123456789123456789',
        })
