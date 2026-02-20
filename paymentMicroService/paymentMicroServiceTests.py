import pytest
import requests

def test_process_payment():
    url = 'http://localhost:8001/process_payment/'
    payload = {
        "userA": {"balance": 100.00, "credit_card": {"card_number": "1234567890123456", "expiry_date": "12/25"}},           
        "userB": {"balance": 50.00},
        "payment_value": 30.00
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200  
    assert response.json() == {"message": "Payment processed successfully"}         