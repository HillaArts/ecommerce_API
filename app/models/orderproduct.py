from app.extensions import db

class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)
    
    # Relationships
    order = db.relationship('Order', backref=db.backref('order_products', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_products', lazy=True))

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_order': self.price_at_order,
            'product': self.product.to_dict()
        }
