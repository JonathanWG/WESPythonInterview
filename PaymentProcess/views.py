from django.shortcuts import render
from .models import User, CreditCard
from .serializers import UserSerializer, CreditCardSerializer
from rest_framework import viewsets
from .utils import PAYMENT_MICROSERVICE_URL
import requests


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self):
    
        user_id = self.queryset.create(user_name='Default User', balance=100.00).user_id
        credit_card = CreditCard.objects.create(user_id=user_id, card_number='0000000000000000', expiry_date='01/25')
        credit_card.save()

        return response

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all(), User.objects.all()
    serializer_class = CreditCardSerializer, UserSerializer

    def create(self, request):
        
        try:
                
            response = super().create(request)

            for q in self.queryset:
                if isinstance(q, CreditCard):
                    credit_card = q.objects.get(user_id=response.data['user_id'])
                    response.data['credit_card'] = {
                        "card_number": credit_card.card_number,
                        "expiry_date": credit_card.expiry_date
                    }
                elif isinstance(q, User):
                    recipient_user = q.objects.get(user_id=response.data['recipient_user_id'])
                    response.data['recipient_balance'] = recipient_user.balance

            # Send payment data to the payment microservice
            payment_data = {
                "userA": {
                    "user_id": response.data['user_id'],
                    "balance": response.data['balance'],
                    "credit_card": {
                        "card_number": response.data['credit_card']['card_number'],
                        "expiry_date": response.data['credit_card']['expiry_date']
                    }
                },  
                "userB": {
                    "user_id": response.data['recipient_user_id'],
                    "balance": response.data['recipient_balance'],
                    "credit_card": "No credit card on file"
                },
                "payment_value": response.data['amount']
            }

            microservice_response =requests.post(PAYMENT_MICROSERVICE_URL, json=payment_data)

            if microservice_response.status_code == 200:
                response.data['payment_status'] = microservice_response.json().get('message', 'Payment processed successfully')

                payment_data = microservice_response.json()
                if 'new_balanceA' in payment_data and 'new_balanceB' in payment_data:
                    response.data['new_balanceA'] = payment_data['userA']['balance'] 
                    response.data['new_balanceB'] = payment_data['userB']['balance']

                    
            else:
                response.data['payment_status'] = 'Payment processing failed'
                

            return response
        
        except (ValueError, KeyError, requests.exceptions.RequestException) as e:

            print(f"Error processing payment: {e}")
            return {"message": "An error occurred while processing the payment", "error": str(e)}
        


class FeedViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        feed_service = 
        return response