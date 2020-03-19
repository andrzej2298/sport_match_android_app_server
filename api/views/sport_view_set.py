from rest_framework import viewsets
from api.models.sport import Sport
from api.serializers.sport_serializer import SportSerializer
from rest_framework.permissions import AllowAny

class SportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sports to be viewed or edited.
    """
    queryset = Sport.objects.all()
    serializer_class = SportSerializer