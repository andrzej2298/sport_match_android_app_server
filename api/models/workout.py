from django.db import models
from django.contrib.gis.db import models as geo_models
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import WORKOUT_GENDER_PREFERENCES, EITHER

PROFICIENCY_VALIDATORS = [MinValueValidator(2), MaxValueValidator(10)]

class Workout(geo_models.Model):
    name = models.CharField(max_length=50)
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
    preferred_gender = models.CharField(
        max_length=1,
        choices=WORKOUT_GENDER_PREFERENCES,
        default=EITHER,
    )
    # postgis adds an index by default to geo fields,
    # normally an index on the location field
    # would have to be added to Meta to prevent full scans of the table
    location = geo_models.PointField()
    max_people = models.IntegerField(validators=[MinValueValidator(2)], null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name
