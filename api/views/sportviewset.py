from rest_framework import viewsets
from api.models.sport import Sport
from api.serializers.sportserializer import SportSerializer

class SportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sports to be viewed or edited.
    """
    queryset = Sport.objects.all()
    serializer_class = SportSerializer