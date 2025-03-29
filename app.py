from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory fake database (for now)
transactions = []

# Root route
@app.route("/")
def home():
    return "Welcome to Auto Finance Manager!"

# GET all transactions
@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    return jsonify(transactions)

# POST a new transaction
@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    transactions.append(data)
    return jsonify({
        "message": "Transaction added!",
        "data": data
    }), 201

# Run the server
if __name__ == "__main__":
    app.run(debug=True)

