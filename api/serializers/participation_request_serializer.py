from rest_framework import serializers
from ..models.participation_request import ParticipationRequest
from .user_serializer import BasicDataUserSerializer


class ParticipationRequestSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # can't ask to join your own workout
        if 'workout' in attrs and 'user' in attrs and attrs['workout'].user == attrs['user']:
            raise serializers.ValidationError('request user can\'t be the same as workout user')

        return attrs

    class Meta:
        model = ParticipationRequest
        fields = '__all__'


class ExpandedParticipationRequestSerializer(ParticipationRequestSerializer):
    user = BasicDataUserSerializer()
