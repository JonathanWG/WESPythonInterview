from django.db import models

from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):
        return self.username


class CreditCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5) #MM/YY

    def __str__(self):
        return f"Card ending in {self.card_number[-4:]}"