from flask import Blueprint, jsonify, request
from ..models import Transaction
from datetime import datetime
from ..db import db

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions])

@transactions_bp.route('', methods=['POST'])
def add_transaction():
    data = request.get_json()

    try:
        transaction = Transaction(
            ticker=data['ticker'],
            isin=data['isin'],
            quantity=data['quantity'],
            price=data['price'],
            fees=data.get('fees', 0.0),
            type=data['type'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            broker=data.get('broker', '')
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@transactions_bp.route('/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get(id)

    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        return '', 204  # No Content

    return jsonify({'error': 'Transaction not found'}), 404

@transactions_bp.route('/<int:id>', methods=['PUT'])
def update_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    # Mise à jour des champs modifiables si présents dans le JSON
    if 'ticker' in data:
        transaction.ticker = data['ticker']
    if 'isin' in data:
        transaction.isin = data['isin']
    if 'quantity' in data:
        transaction.quantity = data['quantity']
    if 'price' in data:
        transaction.price = data['price']
    if 'fees' in data:
        transaction.fees = data['fees']
    if 'type' in data:
        transaction.type = data['type']
    if 'date' in data:
        try:
            transaction.date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Date format should be YYYY-MM-DD'}), 400
    if 'broker' in data:
        transaction.broker = data['broker']

    try:
        db.session.commit()
        return jsonify(transaction.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500