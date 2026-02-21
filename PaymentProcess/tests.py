from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from Users.models import User
from .services import PaymentService

class PaymentTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create(username="Alice", balance=100.00)
        self.bob = User.objects.create(username="Bob", balance=50.00)

    @patch('requests.post')
    def test_execute_payment_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "new_balanceA": 70.00,
            "new_balanceB": 80.00,
            "method": "balance",
            "message": "Success"
        }

        result = PaymentService.execute_payment(
            self.alice.user_id, self.bob.user_id, 30.00, "Coffee"
        )

        self.alice.refresh_from_db()
        assert self.alice.balance == 70.00
        assert result['status'] == "Success"