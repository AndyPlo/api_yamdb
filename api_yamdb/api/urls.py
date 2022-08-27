from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import CommentViewSet, ReviewViewSet

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)', CommentViewSet
)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
