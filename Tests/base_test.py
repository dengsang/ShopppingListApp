import unittest
from flask import Flask
# from unittest import TestCase
# import os
# import config
# import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # os.path.join(app.config['BASEDIR'])

        self.app = app.test_client()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass

    def signup(self, email, username, password, confirm):
        return self.app.post(
            '/signup',
            data=dict(email=email, username=username, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_signup_form_displays(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)

    def test_valid_user_registration(self):
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', 'confirm')
        self.assertIn(b'success', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', 'confirm')
        self.assertIn(b'User (email) already registered', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', '')
        self.assertIn(b'user not found', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'wrong username/password combination', response.data)

    def test_valid_login(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIn(b'success', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIn(b'wrong username/password combination', response.data)

    def test_valid_logout(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/login', follow_redirects=True)
        self.login('email', 'password')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'success', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'user not found', response.data)

    def test_dashboard(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'email', response.data)
        self.assertIn(b'Welcome to Shopping App', response.data)

    def test_dashboard_after_logging_in(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.login('email', 'password')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'email', response.data)
        self.assertIn(b'Welcome to Shopping App', response.data)

    def test_dashboard_without_logging_in(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fdashboard', response.data)


if __name__ == '__main__':
    unittest.main()
