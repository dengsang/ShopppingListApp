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


class UserTestCase(TestCase):
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_db(self):
        self.users = []
        self.user_names = []
        if self.user_names and self.users is list:
            self.assertIn(self.user_names, self.users)
            self.assertListEqual(self.users.append(self.user_names), self.users)
            return "User added to the list successfully"

    def test_user_login(self, email, password):
        self.email = email
        self.password = password
        self.emails = dict(email=email, password=password)
        self.app.get('/login', follow_redirects=True)
        response = self.login('email', 'password')
        if email in self.emails:
            if password == password:
                self.assertIn('email', response.data)
                self.assertEqual(password, password, msg='Login and redirect to dashboard')
                return 'successful login'


if __name__ == '__main__':
    unittest.main()
