from django.db import models

from django.db import models
from Users.models import User

class Activity(models.Model):
    PAYMENT = 'PAY'
    FRIENDSHIP = 'FRND'

    EVENT_TYPES = [
        (PAYMENT, 'Payment'),
        (FRIENDSHIP, 'Friendship'),
    ]
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_initiated')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_received')
    event_type = models.CharField(max_length=4, choices=EVENT_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    content = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} -> {self.event_type} -> {self.target}"