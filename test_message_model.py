"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py

import os
from unittest import TestCase
from datetime import datetime

# from sqlalchemy.exc import IntegrityError

from models import db, Message, User, Like

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        user = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="password",
            image_url='',
            bio='',
            location='')

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Create test client, add sample data."""
        Message.query.delete()
        User.query.delete()

        db.session.commit()

    def test_message_model(self):
        user = User.query.first()
        m = Message(text="Cake", timestamp=datetime.now(), user_id=user.id)
        db.session.add(m)
        db.session.commit()
        self.assertIsInstance(Message.query.get(m.id), Message)

    def test_is_liked_method(self):
        user = User.query.first()
        m = Message(text="Cake", timestamp=datetime.now(), user_id=user.id)
        db.session.add(m)
        db.session.commit()
        self.assertFalse(m.is_liked(user.id))
        like = Like(user_id=1, message_id=m.id)
        db.session.add(like)
        db.session.commit()
        self.assertTrue(m.is_liked(user.id))

    # def test_cascade_delete(self):
    #     user = User.query.first()
    #     m = Message(text="Cake", timestamp=datetime.now(), user_id=user.id)
    #     db.session.add(m)
    #     db.session.commit()
    #     message_id = m.id
    #     self.assertIsInstance(Message.query.get(m.id), Message)
    #     import pdb
    #     pdb.set_trace()
    #     db.session.delete(user)
    #     db.session.commit()
    #     self.assertFalse(Message.query.get(message_id))
