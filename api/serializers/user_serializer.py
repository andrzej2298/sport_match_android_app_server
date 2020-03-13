from api.models.user import User
from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='auth_user.username', read_only=False)
    password = serializers.CharField(source='auth_user.password', read_only=False, write_only=True)
    email = serializers.CharField(source='auth_user.email', read_only=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'birth_date', 'gender', ]

    def update(self, instance, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        super().update(instance, validated_data)

        auth_user = instance.auth_user
        for attr, value in auth_user_data.items():
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
