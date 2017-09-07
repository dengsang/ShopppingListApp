import unittest
from flask import Flask


class TestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

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

    def test_valid_user_registration(self):
        users = []
        user = {'items': '', 'quantity': '', 'price':''}
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', 'confirm')
        self.assertIn(users.append(user), response.data)
        # return "success"

    def test_duplicate_email_user_registration_error(self):
        emails = []
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', 'confirm')
        self.assertIn(emails in list, response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', '')
        self.assertIn('', response.data)

    def test_valid_login(self):
        users = []
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIn(users['password'] == users['password'], response.data)

    def test_login_without_registering(self):
        emails = []
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIsNot(emails in list, response.data)

    def test_invalid_logout_within_being_logged_in(self):
        users = []
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(users is not list, response.data)
        # return "user is not logged in"

    def test_dashboard(self):
        users = []
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(users in list, response.data)
        # return "Welcome to Shopping App dashboard"

    def test_dashboard_after_logging_in(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.login('email', 'password')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        # self.assertIn('Welcome to Shopping App', response.data)
        # return "Welcome to Shopping App"

    def test_dashboard_without_logging_in(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        # return "You should be redirected automatically to target URL:"
        # self.assertIn('You should be redirected automatically to target URL:', response.data)


if __name__ == '__main__':
    unittest.main()
