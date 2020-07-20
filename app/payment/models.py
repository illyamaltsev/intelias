from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.payment.settings import CurrencyCode

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Enum(CurrencyCode), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)

    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
