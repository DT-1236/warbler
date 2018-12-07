"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, User, Message, FollowersFollowee

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

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        user = User.query.get(u.id)
        self.assertIsInstance(user, User, "Query result is a user")

    def test_user_constraints(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD")
        self.assertRaises(IntegrityError, db.session.add(u))
        db.session.rollback()
        u = User(
            email="test2@test.com",
            username="testuser",
            password="HASHED_PASSWORD")
        self.assertRaises(IntegrityError, db.session.add(u))
        db.session.rollback()

    def test_user_repr(self):
        """Does it give back the expected text>"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD")

        self.assertIn("<User #", repr(u), "<User # is in the repr output")
        self.assertIn(": testuser, test@test.com", repr(u),
                      "Email and username are in the repr output")

    def test_following_mapping(self):
        """Do our mappings/relationships work"""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD")
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD")

        db.session.add_all([user1, user2])
        db.session.commit()
        # user2 is following user1
        db.session.add(
            FollowersFollowee(followee_id=user2.id, follower_id=user1.id))
        db.session.commit()
        self.assertIn(user2, user1.followers,
                      "User 2 is part of user1's follower list")

    def test_is_following(self):
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD")
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD")

        db.session.add_all([user1, user2])
        db.session.commit()
        # user2 is following user1
        db.session.add(
            FollowersFollowee(followee_id=user2.id, follower_id=user1.id))
        db.session.commit()

        self.assertTrue(user2.is_following(user1))
        self.assertFalse(user1.is_following(user2))

    def test_is_followed_by(self):
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD")
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD")

        db.session.add_all([user1, user2])
        db.session.commit()
        # user2 is following user1
        db.session.add(
            FollowersFollowee(followee_id=user2.id, follower_id=user1.id))
        db.session.commit()

        self.assertTrue(user1.is_followed_by(user2))
        self.assertFalse(user2.is_followed_by(user1))

    def test_user_signup(self):
        user = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="password",
            image_url='',
            bio='',
            location='')

        db.session.add(user)
        db.session.commit()

        self.assertIsInstance(User.query.get(user.id), User)

    def test_authenticate(self):
        user = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="password",
            image_url='',
            bio='',
            location='')

        db.session.add(user)
        db.session.commit()
        self.assertIsInstance(User.authenticate("testuser1", "password"), User)
        self.assertEqual(
            User.authenticate("testuser1", "password").id, user.id)
        self.assertFalse(User.authenticate("testuser1", "wrong_password"))
