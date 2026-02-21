from rest_framework import viewsets
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer

class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        feed_messages = [item['display_text'] for item in serializer.data]
        return Response(feed_messages)