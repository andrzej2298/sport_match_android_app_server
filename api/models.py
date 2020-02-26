from django.db import models
from django.contrib.gis.db import models as geo_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.constraints import UniqueConstraint

MALE = 'M'
FEMALE = 'F'
EITHER = 'E'
GENDERS = [
    (MALE, 'male'),
    (FEMALE, 'female'),
]
WORKOUT_GENDER_PREFERENCES = GENDERS + [(EITHER, 'either')]

PROFICIENCY_VALIDATORS = [MinValueValidator(2), MaxValueValidator(10)]

class User(models.Model):
    login = models.CharField(max_length=20)
    birth_date = models.DateField()
    email = models.EmailField()
    # TODO phone_number (probably using an external library to validate it)

    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
    )

    def __str__(self):
        return self.login

    def natural_key(self):
        return self.login


class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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
    max_people = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name
