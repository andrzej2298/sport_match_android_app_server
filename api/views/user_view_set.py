from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.user import User
from api.serializers.user_serializer import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import mixins


# TODO permissions
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_object(self):
    #     from sys import stderr
    #     pk = self.request.parser_context['kwargs']['pk']
    #     if pk == 'me':
    #         return User.objects.get(id=self.request.user.id)
    #     else:
    #         try:
    #             user_id = int(pk)
    #             user = User.objects.get(id=user_id)
    #             print(user, file=stderr)
    #             return user
    #         except ValueError:
    #             return None

    @action(methods=['get'], detail=False)
    def me(self, request):
        queryset = User.objects.get(id=request.user.id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def update_me(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = UserSerializer(instance, data=request.data, partial=kwargs['partial'])
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # TODO put and patch currently don't work properly
    #   it seems that changing the password breaks some things
    #   changing the username should also probably be disallowed
    @me.mapping.patch
    def partial_update_me(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_me(request, *args, **kwargs)

    @me.mapping.put
    def full_update_me(self, request, *args, **kwargs):
        import sys
        print(request.user.id, file=sys.stderr)
        print(self.request.user.id, file=sys.stderr)
        kwargs['partial'] = False
        return self.update_me(request, *args, **kwargs)


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer


user_info = {
    'id': 1,
    'username': 'example',
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
}

basic_info = {
    'id': 1,
    'username': 'Ja7000',
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
    'description': 'Oto ja',
    'phone_number': '+48123456789',
    'age': 33,
}


class MockUserViewset(viewsets.ViewSet):
    """
    API endpoint that allows users to update their info.
    """
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        return Response(basic_info)

    @action(methods=['get', 'put', 'patch'], detail=False)
    def me(self, request):
        return Response(user_info)
