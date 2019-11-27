import unittest

from server import app

from model import db, example_data, connect_to_db

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


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

    def test_profile_page(self):

        result = self.client.get("/profile", follow_redirects=True)
        self.assertIn(b"Texting enabled", result.data)


# class TestDataBase(unittest.TestCase):

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True
       
#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb") #create testdb based on model.py

#         # # Create tables and add sample data
#         db.create_all()
#         example_data()


#     def tearDown(self):
#         """Stuff to do after each test."""
#         db.session.close()
#         db.drop_all()
#         pass


#     def test_history_page(self):
#         """Can we reach the history page?"""

#         result = self.client.get("/history", follow_redirects=True)
#         self.assertIn(b"History of Journal Entries", result.data)


#     def test_single_entry_page(self):
#         """Can we reach the history page?"""

#         result = self.client.get("/view-entry/<int:entry_id>", follow_redirects=True)
#         self.assertIn(b"Entry date", result.data)



if __name__ == "__main__":
    unittest.main()


