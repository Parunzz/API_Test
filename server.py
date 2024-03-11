from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data for testing
users = {
    'user1': {'username': 'user1', 'password': 'pass1'},
    'user2': {'username': 'user2', 'password': 'pass2'}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username in users and users[username]['password'] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Initial balance
balance = 0

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    data = request.get_json()
    amount = data.get('amount', 0)
    balance += amount
    return jsonify({'message': f'Deposited {amount} successfully'}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    data = request.get_json()
    amount = data.get('amount', 0)
    if amount > balance:
        return jsonify({'message': 'Insufficient funds'}), 400
    balance -= amount
    return jsonify({'message': f'Withdrawn {amount} successfully'}), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({'balance': balance}), 200

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    thai_text = data['thai_text']
    # Dummy translation, replace with actual translation logic
    english_text = thai_text + " (translated)"
    return jsonify({'english_text': english_text}), 200

if __name__ == '__main__':
    app.run(debug=True)
