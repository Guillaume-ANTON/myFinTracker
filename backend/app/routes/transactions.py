from flask import Blueprint, jsonify
from ..models import Transaction

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions])


