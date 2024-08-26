from datetime import datetime
import pytz
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from app.extensions import db
from app.models.orderproduct import OrderProduct

class Order(db.Model):
    """
    Represents an order placed by a user.
    
    Attributes:
        id (int): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        created_at (datetime): The timestamp when the order was created.
        status (str): The current status of the order.
        user (User): The user who placed the order.
        order_products (list[OrderProduct]): The products associated with the order.
        total_price (float): The total price of the order, calculated dynamically.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Nairobi')))
    status = db.Column(db.String(20), default='Pending')
    
    # Relationships with descriptive backref names
    user = db.relationship('User', backref=db.backref('user_orders', lazy=True))
    order_products = db.relationship('OrderProduct', backref='associated_order', cascade="all, delete-orphan", lazy=True)

    # Calculate total price dynamically
    total_price = column_property(
        select(func.sum(OrderProduct.quantity * OrderProduct.price_at_order))
        .where(OrderProduct.order_id == id)
        .correlate_except(OrderProduct)
        .scalar_subquery()
    )

    def to_dict(self):
        """
        Convert the Order instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Order instance.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'products': [op.to_dict() for op in self.order_products]
        }