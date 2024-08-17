# setup_db.py
from app import create_app, db

app = create_app()
with app.app_context():
    # Perform database operations here
    db.create_all()