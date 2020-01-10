from django.db import models
from django.contrib.gis.db import models as geo_models


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


class Workout(geo_models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    name = geo_models.CharField(max_length=50)
    location = geo_models.PointField()

    def __str__(self):
        return self.name
