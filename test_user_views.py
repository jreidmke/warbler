"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.user = User(
            username="testuser",
            email="test@test.com",
            password="password",
            location='Milwaukee, WI',
            image_url=None,
            bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        )

        self.data = {
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password,
            'location': self.user.location,
            'image_url': self.user.image_url,
            'bio': self.user.bio
        }

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_user_registration_view(self):
        resp = self.client.post('/signup', data=self.data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn(self.user.username, html)

    def test_user_authentication_views(self):
        data = {
            'username': self.user.username,
            'password': self.user.password
        }
        resp = self.client.post('/login', data = data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn(self.user.username, html)
