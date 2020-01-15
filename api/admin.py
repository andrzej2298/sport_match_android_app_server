from django.contrib import admin
from .models import User, Sport, UserSport, Workout

admin.site.register(User)
admin.site.register(Sport)
admin.site.register(UserSport)
admin.site.register(Workout)

