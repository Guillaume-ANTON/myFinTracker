from flask import Blueprint, jsonify
import yfinance as yf

market_bp = Blueprint('market', __name__, url_prefix='/prices')

@market_bp.route('/<string:isin>', methods=['GET'])
def get_price(isin):
    try:
        ticker = isin.upper()
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1d')
        
        if hist.empty:
            return jsonify({"error": "No data found for ticker"}), 404

        price = hist['Close'].iloc[-1]
        return jsonify({"isin": isin, "price": round(price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
