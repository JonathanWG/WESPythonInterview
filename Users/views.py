from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer
from .services import UsersService

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('user_name')
        balance = request.data.get('balance', 100.00)

        if not username:
            return Response({"error": "user_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UsersService.create_user(username=username, initial_balance=balance)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        """
        URL: POST /api/users/{id}/add_friend/
        """
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({"error": "friend_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            UsersService.add_friendship(user_id=pk, friend_id=friend_id)
            return Response({"status": "Friendship established successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)