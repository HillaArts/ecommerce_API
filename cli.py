"""
This module provides a command-line interface for managing the Flask application.
"""

from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    """
    Create the database tables.
    """
    db.create_all()
    print("Database created!")

if __name__ == '__main__':
    cli()