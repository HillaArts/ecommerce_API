from app.extensions import db

class OrderProduct(db.Model):
    """
    Represents the association between an order and a product.
    
    Attributes:
        order_id (int): The ID of the order.
        product_id (int): The ID of the product.
        quantity (int): The quantity of the product in the order.
        price_at_order (float): The price of the product at the time of the order.
        order (Order): The associated order.
        product (Product): The associated product.
    """
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)
    
    # Relationships with descriptive backrefs
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('associated_orders', lazy=True))

    def to_dict(self):
        """
        Convert the OrderProduct instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the OrderProduct instance.
        """
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_order': self.price_at_order,
            'product': self.product.to_dict()
        }