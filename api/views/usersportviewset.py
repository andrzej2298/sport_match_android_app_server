from rest_framework import viewsets
from api.models.usersport import UserSport
from api.serializers.usersportserializer import UserSportSerializer

class UserSportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user's sports to be viewed or edited.
    """
    queryset = UserSport.objects.all()
    serializer_class = UserSportSerializer