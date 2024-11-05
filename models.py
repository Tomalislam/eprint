from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    files = db.Column(db.Text, nullable=False)  # JSON স্ট্রিং হিসাবে ফাইল তথ্য
