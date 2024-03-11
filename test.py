import pytest
import requests

BASE_URL = "http://localhost:5000"

# 1 Authentication: Valid login
def test_valid_login():
    url = f"{BASE_URL}/login"
    payload = {'username': 'user1', 'password': 'pass1'}
    response = requests.post(url, json=payload)
    assert response.status_code == 200

# 2 Authentication: Invalid username
def test_invalid_username():
    url = f"{BASE_URL}/login"
    payload = {'username': 'invalid_username', 'password': 'valid_password'}
    response = requests.post(url, json=payload)
    assert response.status_code == 401

# 3 Authentication: Invalid password
def test_invalid_password():
    url = f"{BASE_URL}/login"
    payload = {'username': 'valid_user', 'password': 'invalid_password'}
    response = requests.post(url, json=payload)
    assert response.status_code == 401

# 4 Authentication: Missing credentials
def test_missing_credentials():
    url = f"{BASE_URL}/login"
    payload = {}  # Missing credentials
    response = requests.post(url, json=payload)
    assert response.status_code == 500

# 5 HTTP Status: Check response status
def test_response_status_200():
    url = f"{BASE_URL}/balance"
    response = requests.get(url)
    assert response.status_code == 200
    
# 6 Idempotent: Check idempotent property
def test_idempotent_property():
    # Making multiple deposit requests with the same amount
    for _ in range(3):
        response = requests.post(f'{BASE_URL}/deposit', json={'amount': 100})
        assert response.status_code == 200
    # Checking the balance to ensure it's consistent
    balance_response = requests.get(f'{BASE_URL}/balance')
    assert balance_response.status_code == 200
    balance_data = balance_response.json()
    assert balance_data['balance'] == 300

# 7: Safe property
def test_safe_property():
    initial_balance_response = requests.get(f'{BASE_URL}/balance')
    assert initial_balance_response.status_code == 200
    initial_balance_data = initial_balance_response.json()
    initial_balance = initial_balance_data['balance']

    # Making a GET request which should not modify the server state
    response = requests.get(f'{BASE_URL}/balance')
    assert response.status_code == 200
    balance_response = requests.get(f'{BASE_URL}/balance')
    assert balance_response.status_code == 200
    balance_data = balance_response.json()
    assert balance_data['balance'] == initial_balance

# 8: Thai to English translation
def test_reversed_text():
    thai_text = "สวัสดี"
    response = requests.post(f'{BASE_URL}/reversed_text', json={'thai_text': thai_text})
    assert response.status_code == 200
    translation_data = response.json()
    assert 'reversed_text' in translation_data
    reversed_thai_text = thai_text[::-1]
    assert reversed_thai_text in translation_data['reversed_text']

# 9: Check response format
def test_response_format():
    # Making a deposit request with missing amount parameter
    response = requests.post(f'{BASE_URL}/deposit', json={})
    assert response.status_code == 200
    deposit_data = response.json()
    assert 'message' in deposit_data

# 10: Attempt to withdraw an amount larger than the current balance
def test_withdrawal_greater_than_balance():
    # Assume initial balance is 500
    initial_balance_response = requests.get(f'{BASE_URL}/balance')
    assert initial_balance_response.status_code == 200
    initial_balance_data = initial_balance_response.json()
    initial_balance = initial_balance_data['balance']

    # Attempt to withdraw an amount larger than the balance
    withdrawal_amount = initial_balance + 100
    withdrawal_response = requests.post(f'{BASE_URL}/withdraw', json={'amount': withdrawal_amount})
    assert withdrawal_response.status_code == 400

    # Verify that the balance remains unchanged
    final_balance_response = requests.get(f'{BASE_URL}/balance')
    assert final_balance_response.status_code == 200
    final_balance_data = final_balance_response.json()
    final_balance = final_balance_data['balance']
    assert final_balance == initial_balance
