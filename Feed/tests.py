from django.test import TestCase
from Users.models import User
from .models import Activity
from .serializers import ActivitySerializer

class FeedTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="Bobby", balance=100)
        self.u2 = User.objects.create(username="Carol", balance=100)

    def test_payment_feed_format(self):
        activity = Activity.objects.create(
            actor=self.u1, target=self.u2, event_type='PAY', amount=5.00, content="Coffee"
        )
        serializer = ActivitySerializer(activity)
        assert serializer.data['display_text'] == "Bobby paid Carol $5.00 for Coffee"

    def test_friendship_feed_format(self):
        activity = Activity.objects.create(
            actor=self.u1, target=self.u2, event_type='FRND'
        )
        serializer = ActivitySerializer(activity)
        assert serializer.data['display_text'] == "Bobby and Carol are now friends"