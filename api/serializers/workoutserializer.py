from api.models.workout import Workout
from rest_framework import serializers
from .userserializer import UserSerializer
from .sportserializer import SportSerializer

class WorkoutSerializer(serializers.ModelSerializer):
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
