from django.urls import path, include
from rest_framework import routers
from .views.login_view_set import LoginView
from .views.user_view_set import UserViewSet, CreateUserViewSet
from .views.workout_view_set import WorkoutViewSet, MatchingWorkoutViewSet
from .views.sport_view_set import SportViewSet
from .views.user_sport_view_set import UserSportViewSet

from .views.user_view_set import MockUserViewset
from .views.login_view_set import MockLoginViewSet
from .views.register_view_set import MockRegisterViewSet
from .views.workout_view_set import MockWorkoutViewSet
from .views.participation_request_viewset import MockParticipationRequestViewSet

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

router.register(r'register', CreateUserViewSet)
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
    path('login/', LoginView.as_view()),
]
