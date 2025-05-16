from .transactions import transactions_bp
from .market import market_bp
from .portfolio import portfolio_bp
def register_routes(app):
    app.register_blueprint(transactions_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(portfolio_bp)