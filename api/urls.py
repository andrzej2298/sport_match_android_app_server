from django.urls import path, include
from rest_framework import routers
from .views.userviewset import UserViewSet
from .views.workoutviewset import WorkoutViewSet, MatchingWorkoutViewSet
from .views.sportviewset import SportViewSet
from .views.usersportviewset import UserSportViewSet
from .views.helloauthviewset import HelloView
from .views.loginview import LoginView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'sports', SportViewSet)
router.register(r'user_sports', UserSportViewSet)
router.register(
    r'matching_workouts',
    MatchingWorkoutViewSet,
    basename='matching_workouts'
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('hello', HelloView.as_view()),
    path('login', LoginView.as_view()),
]

