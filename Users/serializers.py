from rest_framework import serializers
from .models import User, CreditCard

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['card_id', 'card_number', 'expiry_date']

class UserSerializer(serializers.ModelSerializer):
    friends = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'balance', 'friends']
        read_only_fields = ['balance']