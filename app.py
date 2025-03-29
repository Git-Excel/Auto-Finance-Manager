from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    type = db.Column(db.String(20))

# Create DB (only needs to run once)
with app.app_context():
    db.create_all()

# Routes
@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "amount": t.amount,
            "category": t.category,
            "type": t.type
        } for t in transactions
    ])

@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        category=data['category'],
        type=data['type']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction saved!", "data": data}), 201

@app.route("/")
def home():
    return "Welcome to Auto Finance Manager Backend!"

if __name__ == "__main__":
    app.run(debug=True)
