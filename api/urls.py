from django.urls import path, include
from rest_framework import routers
from .views.loginviewset import LoginView
from .views.userviewset import UserViewSet, MockUserViewset
from .views.workoutviewset import WorkoutViewSet, MatchingWorkoutViewSet
from .views.sportviewset import SportViewSet
from .views.usersportviewset import UserSportViewSet
from .views.helloauthviewset import HelloView

from .views.loginviewset import MockLoginViewSet
from .views.registerviewset import MockRegisterViewSet
from .views.workoutviewset import MockWorkoutViewSet
from .views.participationrequestviewset import MockParticipationRequestViewSet

mock_router = routers.DefaultRouter()
router = routers.DefaultRouter()

mock_router.register(r'login', MockLoginViewSet, basename='login')
mock_router.register(r'register', MockRegisterViewSet, basename='register')
mock_router.register(r'users', MockUserViewset, basename='users')
mock_router.register(r'workouts', MockWorkoutViewSet, basename='workouts')
mock_router.register(
    r'participation_requests', MockParticipationRequestViewSet,
    basename='participation_requests'
)

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
    path('mock/', include(mock_router.urls)),
    path('hello', HelloView.as_view()),
    path('login', LoginView.as_view()),
]
