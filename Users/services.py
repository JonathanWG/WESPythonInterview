from django.db import transaction
from .models import User
from Feed.services import FeedService

class UsersService:
    @staticmethod
    def create_user(username, initial_balance=0.00):
        return User.objects.create(username=username, balance=initial_balance)

    @staticmethod
    def add_friendship(user_id, friend_id):
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().get(user_id=user_id)
                friend = User.objects.select_for_update().get(user_id=friend_id)
                if user == friend:
                    raise ValueError("A User not be a self friend.")

                user.friends.add(friend)

                FeedService.log_activity(
                    actor=user, 
                    target=friend, 
                    event_type='FRND'
                )

                return user
        except User.DoesNotExist:
            raise ValueError("Some of the users do not exist.")