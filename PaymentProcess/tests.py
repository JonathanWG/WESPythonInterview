from http import client
from django.test import TestCase

# Create your tests here.
def test_create_user():
    conn = client.HTTPConnection('localhost:8001')
    payload = '{"user_name": "Alice", "balance": 100.00}'
    headers = {'Content-Type': 'application/json'}
    conn.request('POST', '/payment_service/create_user/', payload, headers)
    response = conn.getresponse()
    assert response.status == 201
    assert response.read() == b'{"user_id": 1, "user_name": "Alice", "balance": 100.0}'

def test_process_payment():
    conn = client.HTTPConnection('localhost:8001')
    payload = '{"user_id": 1, "recipient_user_id": 2, "amount": 50.00}'
    headers = {'Content-Type': 'application/json'}
    conn.request('POST', '/payment_service/process_payment/', payload, headers)
    response = conn.getresponse()
    assert response.status == 200
    assert response.read() == b'{"payment_status": "success", "transaction_id": "12345"}'