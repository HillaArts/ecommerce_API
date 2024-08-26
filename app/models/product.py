from datetime import datetime
import pytz
from app.extensions import db

class Product(db.Model):
    """
    Represents a product in the inventory.
    
    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        description (str): A description of the product.
        price (float): The price of the product.
        stock (int): The stock quantity of the product.
        created_at (datetime): The timestamp when the product was created.
        order_products (list[OrderProduct]): The orders associated with the product.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Nairobi')))
    
    # Relationships with a descriptive backref
    order_products = db.relationship('OrderProduct', backref='associated_product', lazy=True)

    def to_dict(self):
        """
        Convert the Product instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Product instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'created_at': self.created_at.isoformat()
        }