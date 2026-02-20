from django.db import models

from django.db import models
from Users.models import User

class Transaction(models.Model):

    sender = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='sent_transactions'
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='received_transactions'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    
    PAYMENT_METHOD_CHOICES = [
        ('BALANCE', 'Wallet Balance'),
        ('CREDIT_CARD', 'External Credit Card'),
    ]
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES
    )
    
    external_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"TX {self.id}: {self.sender} -> {self.recipient} (${self.amount})"