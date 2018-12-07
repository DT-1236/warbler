"""User View tests."""

# run these tests like:
#
#    python -m unittest test_user_views.py

import os
from unittest import TestCase
from werkzeug.datastructures import ImmutableMultiDict

# from sqlalchemy.exc import IntegrityError

from models import db, Message, Like, User, FollowersFollowee

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, session

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get(
    'DATABASE_URL', 'postgres:///warbler-test'))
app.config['WTF_CSRF_ENABLED'] = False
app.debug = False
db.drop_all()
db.create_all()
user = User.signup(
    email="test1@test.com",
    username="testuser1",
    password="password",
    image_url='',
    bio='',
    location='')
db.session.add(user)
db.session.commit()


class UserViewTestCase(TestCase):
    """Tests User Views"""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()
        with self.client:
            self.client.get('/')
            if "curr_user" in session and session["curr_user"]:
                self.client.get("/logout")

    def test_login_page(self):
        """Test that the login page displays and functions correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back.", response.data)

    def test_login_and_homepage_display(self):
        """Tests that the homepage renders correctly"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"What's Happening?", response.data)
        response = self.client.post(
            "/login",
            data=dict(username='testuser1', password='password'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"@testuser1", response.data, "Username shows up")
        self.assertIn(b"Hello,", response.data, "Flash shows up")

    def test_signup_page(self):
        """Tests display and function fo the signup page"""
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Join Warbler today.", response.data)
        response = self.client.post(
            "/signup",
            data=dict(
                email="asdf@asdf.com",
                username='testuser2',
                password='password',
                image_url='',
                header_image_url='',
                bio='',
                location=''),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"@testuser2", response.data, "Username shows up")
