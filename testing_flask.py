import unittest

from server import app

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
    
    def tearDown(self):
        """Stuff to do after each test."""

        pass

    def test_index_page(self):
        """Can we reach the root page?"""

        result = self.client.get("/")
        # self.assertEqual(result.status_code, 200)
        self.assertIn(b"Login", result.data)

    def test_create_account_page(self):
        """Can we get to the create account page?"""

        result = self.client.get("/create-account")
        self.assertIn(b"Create Account", result.data)

    def test_home_page(self):
        """Can we reach the homepage?"""

        result = self.client.get("/home", follow_redirects=True)
        self.assertIn(b"On a scale of 1-5", result.data)


    def test_login_page(self):
        """Can we reach the login page?"""

        result = self.client.get("/login", follow_redirects=True)
        self.assertIn(b"Welcome Back!", result.data)


    def test_login_page(self):
        """Can we reach the login page?"""

        result = self.client.get("/login", follow_redirects=True)
        self.assertIn(b"Welcome Back!", result.data)
        
if __name__ == "__main__":
    unittest.main()