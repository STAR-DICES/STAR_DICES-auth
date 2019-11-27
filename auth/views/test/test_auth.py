import unittest
import json

from auth.app import start
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from auth.database import db, User


class TestAuth(TestCase): # pragma: no cover
    def create_app(self):
        self.app = start(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        with self.context:
            db.drop_all()

    def test_login_invalid(self):
        # error: invalid request
        data = { 'email': "example@example.com" }
        reply = self.client.post('/login', json=data)
        self.assertEqual(reply.status_code, 400)

    def test_login_wrong(self):
        # error: wrong pass
        data = { 'email': "example@example.com", 'password': "42" }
        reply = self.client.post('/login', json=data)
        self.assertEqual(reply.status_code, 401)

    def test_login_correct(self):
        # sussess: user and pwd correct
        data = { 
                'email': "example@example.com",
                'password': "admin"
                }
        reply = self.client.post('/login', json=data)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(json.loads(reply.data), { "firstname": "Admin", "user_id": 1 } )

        

    def test_signup_invalid(self):

        # error: invalid request
        # 
        data = { 
                'firstname': "adminadmin",
                'lastname': "admin",
                'password': "giacobbe",
                'dateofbirth': "10/05/2020"
                }
        reply = self.client.post('/signup', json=data)
        self.assertEqual(reply.status_code, 400)

    def test_signup_error(self):
        # error: same email
        # 
        data = { 
                'email': "example@example.com",
                'firstname': "adminadmin",
                'lastname': "admin",
                'password': "giacobbe",
                'dateofbirth': "10/05/2020"
                }
        reply = self.client.post('/signup', json=data)
        self.assertEqual(reply.status_code, 409)

    def test_signup_success(self):
        # success: user and pwd correct
        # 
        data = { 
                'email': "example3@example.com",
                'firstname': "holy10characterspls",
                'lastname': "admin",
                'password': "giacobbe",
                'dateofbirth': "01/04/2006"
                }
        reply = self.client.post('/signup', json=data)
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(json.loads(reply.data), {
                                        'user_id': 3,
                                        'firstname': "holy10characterspls"
                                        })

        
        # # error:signup while logged in
        # reply = self._login('example@example.com', 'admin')
        # self.assertEqual(reply.status_code, 302)
        # reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        # self.assertEqual(reply.status_code, 302)
        # with self.context:
        #     q = User.query.filter_by(email='example3@example.com').first()
        #     self.assertIsNone(q)
        
        # # error:not enough char in password
        # # self._logout()
        # reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        # self.assertEqual(reply.status_code, 200)
        # with self.context:
        #     q = User.query.filter_by(email='example3@example.com').first()
        #     self.assertIsNone(q)
        
        # # success:register user
        # self._signup('example3@example.com', 'holy10characterspls', 'admin', 'giacobbe', '01/04/2006', True)
        # self._login('example3@example.com', 'admin')
        # with self.context:
        #     q = User.query.filter_by(email='example3@example.com').first()
        #     self.assertIsNotNone(q)
            

    def test_user_exists(self):

        # user present in db
        # 
        reply = self.client.get('user-exists/1')
        self.assertEqual(reply.status_code, 200)

        # user non present in db
        # 
        reply = self.client.get('user-exists/999')
        self.assertEqual(reply.status_code, 404)

        # error: user_id not a number
        # 
        reply = self.client.get('user-exists/user')
        self.assertEqual(reply.status_code, 404)
