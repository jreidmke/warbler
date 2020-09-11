"""User model tests."""

import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from models import db, User, Message, Follows, Like

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()
bcrypt = Bcrypt()

class MessageModelTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        self.user = User(
            username="james",
            email="james@test.com",
            password="password",
            location='Milwaukee, WI',
            image_url=None,
            bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        )
        db.session.add(self.user)
        db.session.commit()
        self.msg = Message(
            text='Lorem ipsum dolor sit amet.',
            user_id=self.user.id,
        )

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Like.query.delete()

    def test_message_model(self):
        db.session.add(self.msg)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.msg.user_id, self.user.id)
        self.assertIn('Lorem ipsum dolor', self.msg.text)
        self.assertIn('Lorem ipsum dolor', self.user.messages[0].text)
