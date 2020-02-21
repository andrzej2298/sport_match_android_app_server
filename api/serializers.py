from .models import User, Workout, Sport, UserSport
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'


class UserSportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserSport
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=UserSport.objects.all(),
                fields=['user', 'sport']
            )
        ]


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, attrs):
        if attrs['start'] > attrs['end']:
            raise serializers.ValidationError('end must occur after start')
        return attrs

    class Meta:
        model = Workout
        fields = '__all__'


class WorkoutSerializerExpanded(WorkoutSerializer):
    user = UserSerializer()
    sport = SportSerializer()
