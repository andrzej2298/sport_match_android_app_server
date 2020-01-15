from django.db import models
from django.contrib.gis.db import models as geo_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.constraints import UniqueConstraint


class User(models.Model):
    login = models.CharField(max_length=20)
    birth_date = models.DateField()

    MALE = 'M'
    FEMALE = 'F'
    SEXES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
    ]
    sex = models.CharField(
        max_length=1,
        choices=SEXES,
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
    proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'sport'], name='unique_user_sport')
        ]

    def __str__(self):
        return f'{self.user}\'s {self.sport}'


class Workout(geo_models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    sport = models.ForeignKey(
        'Sport',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    location = geo_models.PointField()  # postgis adds an index by default
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
