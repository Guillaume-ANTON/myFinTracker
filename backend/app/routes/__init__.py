from .transactions import transactions_bp

def register_routes(app):
    app.register_blueprint(transactions_bp)