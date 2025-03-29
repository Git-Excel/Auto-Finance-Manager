from datetime import datetime
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
    date = db.Column(db.DateTime, default=datetime.utcnow)

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
    date = datetime.strptime(data['date'], "%Y-%m-%d") if 'date' in data else datetime.utcnow()
    new_transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        category=data['category'],
        type=data['type'],
        date=date
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction saved!", "data": data}), 201

@app.route("/api/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": f"Transaction {id} deleted."})

@app.route("/api/summary", methods=["GET"])
def get_summary():
    # Get query parameters
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    # Build query based on optional filters
    query = Transaction.query
    if month and year:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        query = query.filter(Transaction.date >= start_date, Transaction.date < end_date)

    transactions = query.all()

    total_income = 0
    total_expense = 0
    category_totals = {}

    for t in transactions:
        if t.type == "income":
            total_income += t.amount
        elif t.type == "expense":
            total_expense += t.amount

        # Group by category
        if t.category in category_totals:
            category_totals[t.category] += t.amount
        else:
            category_totals[t.category] = t.amount

    # Sory categories by amount (highest first), and limit to top 5
    sorted_categories = dict(
        sorted(category_totals.items(), key=lambda item: item[1], reverse=True)[:5]
    )

    summary = {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
        "by_category": sorted_categories
    }

    return jsonify(summary)

@app.route("/")
def home():
    return "Welcome to Auto Finance Manager Backend!"

if __name__ == "__main__":
    app.run(debug=True)
