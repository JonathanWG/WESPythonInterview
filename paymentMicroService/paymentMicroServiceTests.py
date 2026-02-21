import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from paymentMicroService import app 

client = TestClient(app)

def test_process_payment_success():
    payload = {
        "userA": {
            "user_id": 1,
            "balance": 100.00,
            "credit_card": {"card_number": "4234567890123456", "expiry_date": "12/25"}
        },
        "userB": {
            "user_id": 2,
            "balance": 50.00
        },
        "payment_value": 30.00
    }
    response = client.post("/process_payment/", json=payload)
    
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["new_balanceA"] == 70.00
    assert data["new_balanceB"] == 80.00

def test_process_payment_insufficient_funds():
    payload = {
        "userA": {
            "user_id": 1,
            "balance": 10.00,
            "credit_card": None
        },
        "userB": {"user_id": 2, "balance": 50.00},
        "payment_value": 30.00
    }
    response = client.post("/process_payment/", json=payload)
    assert response.status_code == 400


def test_process_payment_exact_balance():
    payload = {
        "userA": {"user_id": 1, "balance": 50.00, "credit_card": None},
        "userB": {"user_id": 2, "balance": 10.00},
        "payment_value": 50.00
    }
    response = client.post("/process_payment/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["method"] == "balance"
    assert data["new_balanceA"] == 0.00

def test_process_payment_invalid_payload():
    payload = {
        "userA": {"user_id": 1, "balance": 100.00},
    }
    response = client.post("/process_payment/", json=payload)
    assert response.status_code == 422