from unittest import TestCase
from flask import url_for
from main_app import create_app, db
from main_app.models import User, Role


class CostAppClientTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(url_for('users.register'), data={
            'email': 'test@test.com',
            'username': 'username',
            'password': 'password',
            'password2': 'password'
        })
        self.assertTrue(response.status_code == 302)

        # login with the new account
        response = self.client.post(url_for('users.login'), data={
            'email': 'test@test.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertTrue(
            b'You have not confirmed your account yet' in response.data)

        # send a confirmation token
        user = User.query.filter_by(email='jtest@test.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('users.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(
            b'Your account is confirmed, Thank you!!!' in response.data)

        # log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(b'You have been logged out!!!' in response.data)
