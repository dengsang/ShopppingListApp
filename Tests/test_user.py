import unittest


class UserTestCase(unittest.TestCase):
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
        self.emails = [email, password]
        if email in self.emails:
            if password == password:
                self.assertEqual(password, password, msg='Login and redirect to dashboard')
                return 'successful login'


if __name__ == '__main__':
    unittest.main()
