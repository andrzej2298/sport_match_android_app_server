from rest_framework import viewsets
from rest_framework.response import Response


class MockRegisterViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to register.
    """
    def create(self, request):
        return Response({
            'id': 1,
            'login': 'example',
            'mail': 'mail@example.com',
            'birth_date': '2020-01-01',
            'sport_list': [
                {
                    'sport_id': 1,
                    'sport_proficiency': 2,
                },
                {
                    'sport_id': 2,
                    'sport_proficiency': 1
                }
            ],
            'gender': 'F',
            'phone_number': '+48111111111',
            'description': 'I like dogs',
            'token': '123456789123456789',
        })
