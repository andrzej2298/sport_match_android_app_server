from api.models.workout import Workout
from api.models.user import User
from api.models.participation_request import ParticipationRequest
from rest_framework import serializers
from .user_serializer import BasicDataUserSerializer
from ..models.constants import ACCEPTED


class BasicWorkoutInputSerializer(serializers.ModelSerializer):
    signed_people = serializers.SerializerMethodField()

    def get_signed_people(self, obj):
        return get_people_signed_for_a_workout(obj.id)

    @staticmethod
    def validate_less_than(smaller_key, greater_key, attrs, error_message):
        if smaller_key in attrs and greater_key in attrs and attrs[smaller_key] > attrs[greater_key]:
            raise serializers.ValidationError(error_message)

    def validate(self, attrs):
        FullWorkoutSerializer.validate_less_than('start_time', 'end_time', attrs, 'end must occur after start')
        FullWorkoutSerializer.validate_less_than('age_min', 'age_max', attrs, 'min age must be smaller than max age')
        return attrs

    class Meta:
        model = Workout
        fields = '__all__'


class BasicWorkoutOutputSerializer(BasicWorkoutInputSerializer):
    user = BasicDataUserSerializer()


def get_people_signed_for_a_workout(workout):
    return 1 + ParticipationRequest.objects.filter(workout=workout, status=ACCEPTED).count()


class FullWorkoutSerializer(BasicWorkoutInputSerializer):
    user_list = serializers.SerializerMethodField()

    def get_user_list(self, obj):
        workout = obj.id
        user = obj.user_id
        participants = {
            request.user for request in
            ParticipationRequest.objects
                .filter(workout=workout, status=ACCEPTED)
                .select_related('user')
        }
        owner = User.objects.get(id=user)
        participants.add(owner)
        return BasicDataUserSerializer(participants, many=True).data
