import unittest
import json

from auth.app import start
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError
from auth.database import db, User
from flask_login import current_user


class TestHelper(TestCase): # pragma: no cover
    def create_app(self):
        self.app = start(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        with self.context:
            db.drop_all()

    def _login(self, email, password, follow_redirects=False):
        return self.client.post('/login', follow_redirects=follow_redirects, data={
            'email': email,
            'password': password
        })

    def _signup(self, email, password, first_name, last_name, birthday, follow_redirects=False):
        return self.client.post('/signup', follow_redirects=follow_redirects, data={
            'email': email,
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'dateofbirth': birthday
        })

    def _logout(self, follow_redirects=False):
        return self.client.get('/logout', follow_redirects=follow_redirects)


    def test_login(self):
        
        # error:wrong pass
        reply = self._login("example@example.com", "42")
        self.assert_context("notlogged", True)
        with self.context:
            q = User.query.filter_by(email="example@example.com")
            self.assertNotEqual(q.first(), current_user)

        # success: logged in
        reply = self._login("example@example.com", "admin")
        self.assertEqual(reply.status_code, 302)
        with self.context:
            q = User.query.filter_by(email="example@example.com").first()
            #self.assertEqual(current_user.id, q.id) # current_user anonymous?
        
    def test_login_redir(self):
    
        # success: logged in, redirected
        reply = self._login("example@example.com", "admin", True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("home.html")
        
    def test_logout(self):
    
        # error:not logged in
        reply = self._logout()
        self.assertEqual(reply.status_code, 401)
        
        # success:logged out, no redir
        reply = self._login("example@example.com", "admin")
        reply = self._logout()
        self.assertEqual(reply.status_code, 302)
        
        # success:logged out, redirected
        reply = self._login("example@example.com", "admin")
        reply = self._logout(True)
        self.assertEqual(reply.status_code, 200)
        self.assert_template_used("login.html")
        
    def test_signup(self):
    
        # error:same email
        self._signup('example@example.com', 'adminadmin', 'admin', 'giacobbe', '01/04/1006')
        self.assert_template_used("create_user.html")
        
        # error:signup while logged in
        reply = self._login('example@example.com', 'admin')
        self.assertEqual(reply.status_code, 302)
        reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        self.assertEqual(reply.status_code, 302)
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNone(q)
        
        # error:not enough char in password
        self._logout()
        reply = self._signup('example2@example.com', 'not10char', 'admin', 'giacobbe', '01/04/1006')
        self.assertEqual(reply.status_code, 200)
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNone(q)
        
        # success:register user
        self._signup('example3@example.com', 'holy10characterspls', 'admin', 'giacobbe', '01/04/2006', True)
        self._login('example3@example.com', 'admin')
        with self.context:
            q = User.query.filter_by(email='example3@example.com').first()
            self.assertIsNotNone(q)
            
                

        
        
