import unittest

from server import app

import os

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


    def test_home_page(self):
        """Can we reach the homepage?"""

        result = self.client.get("/home", follow_redirects=True)
        self.assertIn(b"On a scale of 1-5", result.data)


class TestDataBase(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
       
        # Connect to test database
        connect_to_db(app, "testdb") #create testdb based on model.py

        # # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Stuff to do after each test."""
        db.session.close()
        db.drop_all()

    def test_history_page(self):
        """Can we reach the history page?"""

        result = self.client.get("/history", follow_redirects=True)
        self.assertIn(b"morning", result.data)


    def test_single_entry_page(self):
        """Can we reach the single entry page?"""

        result = self.client.get("/view-entry/1", follow_redirects=True)
        self.assertIn(b"happy, smiley", result.data)


    def test_profile_page(self):
        """Can we reach the profile page?"""

        result = self.client.get("/profile", follow_redirects=True)
        self.assertIn(b"mbear@gmail.com", result.data)


    def test_sentiment_page(self):
        """Are we successfuly making an API request"""

        result = self.client.get("/sentiment-analysis")
        self.assertEqual(result.status_code, 200)


    def  test_happy_page(self):
        """Can we successfully reach the happiness page?"""

        result = self.client.get("/happy")
        self.assertIn(b"Learn about what makes you happy", result.data)


if __name__ == "__main__":
    unittest.main()


