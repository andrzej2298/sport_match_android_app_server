from api.models.workout import Workout
from rest_framework import serializers
from .user_serializer import UserSerializer
from .sport_serializer import SportSerializer


class WorkoutSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_less_than(smaller_key, greater_key, attrs, error_message):
        if smaller_key in attrs and greater_key in attrs and attrs[smaller_key] > attrs[greater_key]:
            raise serializers.ValidationError('end must occur after start')

    def validate(self, attrs):
        WorkoutSerializer.validate_less_than('start_time', 'end_time', attrs, 'end must occur after start')
        WorkoutSerializer.validate_less_than('age_min', 'age_max', attrs, 'min age must be smaller than max age')
        return attrs

    class Meta:
        model = Workout
        fields = '__all__'


class WorkoutSerializerExpanded(WorkoutSerializer):
    user = UserSerializer()
    sport = SportSerializer()
