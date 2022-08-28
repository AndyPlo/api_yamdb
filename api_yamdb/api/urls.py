from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import CommentViewSet, ReviewViewSet
from .views import UserViewSet, SignUpViewSet, GetTokenView

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)', CommentViewSet
)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
# v1_router.register(r'users/me', UserProfileViewSet, basename='profile')
v1_router.register(r'users', UserViewSet)
v1_router.register(r'auth/signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/token/',
        GetTokenView.as_view(),
        name='token_obtain_pair'
    )
]
