from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('users', UserViewSet)

auth_patterns = [
    path('auth/token/', token, name='token'),
    path('auth/signup/', signup, name='signup')
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(auth_patterns))
]
