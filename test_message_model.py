"""User model tests."""

import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()
bcrypt = Bcrypt()