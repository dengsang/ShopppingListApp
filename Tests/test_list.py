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


class AddListTestCase(TestCase):
    def dashboard(self, items, quantity, price):
        return self.app.post(
            '/dashboard',
            data=dict(email=items, password=quantity, price=price),
            follow_redirects=True
        )

    def test_add_list(self):
        self.items = []
        self.user_items = []
        if self.user_items and self.items is list:
            self.assertIn(self.user_items, self.items)
            self.assertListEqual(self.items.append(self.user_items), self.items)
            return "Items added to the shopping list successfully"

    def test_delete_item(self):
        self.items = []
        self.user_items = []
        if self.user_items and self.items is list:
            self.assertIn(self.user_items, self.items)
            self.assertListEqual(self.items.clear(), self.items)
            return "Items deleted successfully"


if __name__ == '__main__':
    unittest.main()
