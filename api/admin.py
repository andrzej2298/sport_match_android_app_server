from django.contrib import admin
from .models.user import User
from .models.sport import Sport
from .models.usersport import UserSport
from .models.workout import Workout

admin.site.register(User)
admin.site.register(Sport)
admin.site.register(UserSport)
admin.site.register(Workout)

