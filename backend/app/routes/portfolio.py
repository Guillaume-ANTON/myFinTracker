from flask import Blueprint, jsonify
from ..models import Transaction
import yfinance as yf
from collections import defaultdict

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('', methods=['GET'])
def get_portfolio():
    transactions = Transaction.query.all()
    holdings = defaultdict(lambda: {"quantity": 0, "total_cost": 0})

    for tx in transactions:
        isin = tx.isin.upper()
        qty = tx.quantity
        price = tx.price

        if tx.type == 'buy':
            holdings[isin]["quantity"] += qty
            holdings[isin]["total_cost"] += qty * price
        elif tx.type == 'sell':
            holdings[isin]["quantity"] -= qty
            holdings[isin]["total_cost"] -= qty * price  # approximation

    portfolio_summary = []

    for isin, data in holdings.items():
        quantity = data["quantity"]
        total_cost = data["total_cost"]
        if quantity <= 0:
            continue  # on ignore les lignes à 0 ou négatives

        avg_price = total_cost / quantity

        try:
            stock = yf.Ticker(isin)
            hist = stock.history(period='1d')
            if hist.empty:
                market_price = None
            else:
                market_price = hist['Close'].iloc[-1]
        except Exception:
            market_price = None

        if market_price:
            current_value = round(quantity * market_price, 2)
            gain = round(current_value - total_cost, 2)
        else:
            current_value = None
            gain = None

        portfolio_summary.append({
            "isin": isin,
            "quantity": quantity,
            "average_price": round(avg_price, 2),
            "market_price": round(market_price, 2) if market_price else None,
            "current_value": current_value,
            "unrealized_gain": gain
        })

    return jsonify(portfolio_summary)