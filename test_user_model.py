"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()
bcrypt = Bcrypt()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        self.user = User(
            username="testuser",
            email="test@test.com",
            password="password",
            location='Milwaukee, WI',
            image_url=None,
            bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        )
        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

    def test_user_model(self):
        """Does basic model work?"""

        db.session.add(self.user)
        db.session.commit()
        u_rep = self.user.__repr__()

        # User should have no messages & no followers
        self.assertEqual(len(self.user.messages), 0)
        self.assertEqual(len(self.user.followers), 0)
        self.assertIn(f'User #{self.user.id}: {self.user.username}, {self.user.email}', u_rep)

    def test_user_registration(self):
        reg_obj = User.signup(username=self.user.username, email=self.user.email, password=self.user.password, location=self.user.location, image_url=self.user.image_url, bio=self.user.bio)
        self.assertEqual(reg_obj.username, self.user.username)

    def test_user_authentication(self):
        reg_obj = User.signup(username=self.user.username, email=self.user.email, password=self.user.password, location=self.user.location, image_url=self.user.image_url, bio=self.user.bio)
        auth_obj = User.authenticate(self.user.username, self.user.password)
        self.assertEqual(auth_obj, reg_obj)

    def test_failed_user_authentication(self):
        User.signup(username=self.user.username, email=self.user.email, password=self.user.password, location=self.user.location, image_url=self.user.image_url, bio=self.user.bio)
        auth_obj = User.authenticate('TESTUSER', 'foo')
        self.assertEqual(auth_obj, False)
