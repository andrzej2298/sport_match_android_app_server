from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser

from api.models.user import User
from api.utils.time import get_current_age
from .user_sport_serializer import UserSportSerializer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='auth_user.username', read_only=False)
    password = serializers.CharField(source='auth_user.password', read_only=False, write_only=True)
    email = serializers.CharField(source='auth_user.email', read_only=False)
    sport_list = UserSportSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'birth_date', 'sport_list', 'gender', 'description', 'phone_number',
            'location'
        ]

    def update(self, instance, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        super().update(instance, validated_data)

        auth_user = instance.auth_user
        for attr, value in auth_user_data.items():
            if attr == 'password':
                auth_user.set_password(value)
            else:
                setattr(auth_user, attr, value)
        auth_user.save()

        return instance

    def create(self, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        username = auth_user_data.pop('username')
        auth_user = DjangoUser.objects.create_user(
            username,
            **auth_user_data,
        )
        user = User.objects.create(
            auth_user=auth_user,
            **validated_data
        )
        return user


class BasicDataUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username'
        ]


class ParticipationRequestUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'location'
        ]


class OtherUserSerializer(UserSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        return get_current_age(obj.birth_date)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'sport_list', 'gender', 'description', 'phone_number', 'age'
        ]
