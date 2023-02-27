from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app=app)
    return db


def create_tables(app):
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    db.metadata.create_all(engine)
    return engine


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, nullable=False)
    buyer = db.Column(db.String(255), nullable=False)
    tracking_code = db.Column(db.String(255), nullable=False, unique=True)
    sender_evaluation = db.Column(db.Text, nullable=True)
    winner_evaluation = db.Column(db.Text, nullable=True)
    date_sended = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    date_received = db.Column(db.DateTime, nullable=True)
    received = db.Column(db.Boolean, default=False, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product,
            "buyer": self.buyer,
            "tracking_code": self.tracking_code,
            "sender_evaluation": self.sender_evaluation,
            "winner_evaluation": self.winner_evaluation,
            "date_sended": self.date_sended,
            "received": self.received,
            "date_received": self.date_received,
        }
