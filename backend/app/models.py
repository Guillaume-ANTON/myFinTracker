from .db import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    fees = db.Column(db.Float, default=0.0)
    type = db.Column(db.String(10), nullable=False)  # buy, sell, dividend
    date = db.Column(db.Date, nullable=False)
    broker = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "quantity": self.quantity,
            "price": self.price,
            "fees": self.fees,
            "type": self.type,
            "date": self.date.isoformat(),
            "broker": self.broker
        }