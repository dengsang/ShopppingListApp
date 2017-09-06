import unittest
# import os
# import config
import app
from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
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
        self.assertIn(b'Thanks for registering!', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', 'confirm')
        self.assertIn(b'ERROR! Email (email) already exists.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        response = self.signup('email', 'username', 'password', '')
        self.assertIn(b'This field is required.', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Need an account?', response.data)
        self.assertIn(b'Forgot your password?', response.data)

    def test_valid_login(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        self.assertIn(b'ERROR! Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/login', follow_redirects=True)
        self.login('email', 'password')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)

    def test_dashboard(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'First time logged in. Welcome!', response.data)

    def test_dashboard_after_logging_in(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('email', 'username', 'password', 'confirm')
        self.app.get('/logout', follow_redirects=True)
        self.login('email', 'password')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'Last Logged In: ', response.data)

    def test_dashboard_without_logging_in(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fuser_profile', response.data)


if __name__ == '__main__':
    unittest.main()
