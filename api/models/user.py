from django.db import models
from .constants import GENDERS
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    auth_user = models.OneToOneField(
        DjangoUser,
        on_delete=models.CASCADE
    )

    # TODO phone_number (probably using an external library to validate it)

    birth_date = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
    )

    def __str__(self):
        return self.auth_user.username

    def natural_key(self):
        return self.auth_user.username
