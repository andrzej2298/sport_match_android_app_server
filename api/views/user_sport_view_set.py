from rest_framework import viewsets
from api.models.user_sport import UserSport
from api.serializers.user_sportserializer import UserSportSerializer

class UserSportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user's sports to be viewed or edited.
    """
    queryset = UserSport.objects.all()
    serializer_class = UserSportSerializer