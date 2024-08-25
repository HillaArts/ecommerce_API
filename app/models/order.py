from datetime import datetime
from app.extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    
    # Relationships with descriptive backref names
    user = db.relationship('User', backref=db.backref('user_orders', lazy=True))
    order_products = db.relationship('OrderProduct', backref='associated_order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'products': [op.to_dict() for op in self.order_products]
        }
