from django.db import models
from .constants import GENDERS

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
