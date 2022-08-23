from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review, Title

from .serializers import ReviewSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()
