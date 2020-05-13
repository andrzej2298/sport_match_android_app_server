from rest_framework import serializers
from api.models.participation_request import ParticipationRequest
from api.models.constants import PENDING, ACCEPTED
from .user_serializer import ParticipationRequestUserSerializer
from .workout_serializer import BasicWorkoutInputSerializer


class ParticipationRequestSerializer(serializers.ModelSerializer):
    def _validate_status_change(self):
        request = self.context['request']
        if request.method == 'PATCH' and 'status' in request.data:
            workout = self.instance.workout
            status = request.data['status']

            # can change status from pending only once
            if status == PENDING:
                raise serializers.ValidationError('can change status from pending only once')

            signed_users = ParticipationRequest.objects.filter(workout=workout, status=ACCEPTED).count() + 1
            # don't allow too many people to be accepted
            if status == ACCEPTED and signed_users >= workout.max_people:
                raise serializers.ValidationError('too many people already in the workout')

    def validate(self, attrs):
        # can't ask to join your own workout
        if 'workout' in attrs and 'user' in attrs and attrs['workout'].user == attrs['user']:
            raise serializers.ValidationError('request user can\'t be the same as workout user')

        self._validate_status_change()

        return attrs

    class Meta:
        model = ParticipationRequest
        exclude = ['seen']


class ExpandedParticipationRequestSerializer(ParticipationRequestSerializer):
    user = ParticipationRequestUserSerializer()
    workout = BasicWorkoutInputSerializer()
