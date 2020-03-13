from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import WORKOUT_GENDER_PREFERENCES, EITHER

PROFICIENCY_VALIDATORS = [MinValueValidator(2), MaxValueValidator(10)]

class UserSport(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    sport = models.ForeignKey(
        'Sport',
        on_delete=models.CASCADE,
    )
    level = models.IntegerField(
        validators=PROFICIENCY_VALIDATORS,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'sport'], name='unique_user_sport')
        ]

    def __str__(self):
        return f'{self.user}\'s {self.sport}'