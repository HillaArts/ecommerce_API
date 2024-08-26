from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    """
    Represents a user in the system.
    
    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        role (str): The role of the user, either 'admin' or 'client'.
        created_at (datetime): The timestamp when the user was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # 'admin' or 'client'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Africa/Nairobi')))

    def set_password(self, password):
        """
        Set the user's password.
        
        Args:
            password (str): The password to be hashed and set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check the user's password.
        
        Args:
            password (str): The password to be checked.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert the User instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the User instance.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
        }