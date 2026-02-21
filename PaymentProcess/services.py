import requests
from django.db import transaction
from Users.models import User
from WESPythonInterview.Feed.services import FeedService
from .models import Transaction
from.utils import PAYMENT_MICROSERVICE_URL

class PaymentService:
    @staticmethod
    def execute_payment(sender_id, recipient_id, amount, description):

        sender = User.objects.get(user_id=sender_id)
        recipient = User.objects.get(user_id=recipient_id)
        card = sender.cards.first()

        payload = {
            "userA": {
                "user_id": sender.user_id,
                "balance": float(sender.balance),
                "credit_card": {
                    "card_number": card.card_number, 
                    "expiry_date": card.expiry_date
                } if card else None
            },
            "userB": {
                "user_id": recipient.user_id, 
                "balance": float(recipient.balance)
            },
            "payment_value": float(amount)
        }

        try:
            resp = requests.post(PAYMENT_MICROSERVICE_URL, json=payload, timeout=5)
            
            if resp.status_code != 200:
                error_detail = resp.json().get("detail", "Payment failed")
                raise Exception(f"Gateway Error: {error_detail}")
            
            data = resp.json()

            with transaction.atomic():
                sender.balance = data['new_balanceA']
                recipient.balance = data['new_balanceB']
                sender.save()
                recipient.save()

                Transaction.objects.create(
                    sender=sender,
                    recipient=recipient,
                    amount=amount,
                    payment_method=data.get('method', 'UNKNOWN').upper(),
                    description=description,
                    external_transaction_id=data.get('transaction_id')
                )

                FeedService.log_activity(
                    actor=sender,
                    target=recipient,
                    event_type='PAY',
                    amount=amount,
                    content=description #(ex: Coffee)
                )

            return {
                "status": data.get("message", "Success"),
                "sender_balance": float(sender.balance),
                "recipient_balance": float(recipient.balance)
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Connection to Payment Gateway failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Payment failed: {str(e)}")