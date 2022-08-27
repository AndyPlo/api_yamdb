from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserProfileViewSet, SignUpViewSet, GetTokenView

v1_router = routers.DefaultRouter()

v1_router.register(r'users/me', UserProfileViewSet, basename='profile')
v1_router.register(r'users', UserViewSet)
v1_router.register(r'auth/signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/token/',
        GetTokenView.as_view(),
        name='token_obtain_pair'
    )
]