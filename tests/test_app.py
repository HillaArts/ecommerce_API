# tests/test_app.py
import unittest
from app import create_app, db
from app.models import User

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('test_config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_login(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

if __name__ == '__main__':
    unittest.main()
