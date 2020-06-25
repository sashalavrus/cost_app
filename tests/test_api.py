from unittest import TestCase
import json
from base64 import b64encode
from flask import url_for
from main_app import create_app, db
from main_app.models import User, Role


class APITestCase(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_no_auth(self):
        response = self.client.get(url_for('api.view_user_costs'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 401)

    def test_bad_auth(self):
        # add a user
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        db.session.add(u)
        db.session.commit()

        # authenticate with bad password
        response = self.client.get(
            url_for('api.view_user_costs'),
            headers=self.get_api_headers('username', 'password'))
        self.assertTrue(response.status_code == 401)

    def test_token_auth(self):
        # add a user
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        u.confirmed = True
        db.session.add(u)
        db.session.commit()

        # issue a request with a bad token
        response = self.client.get(
            url_for('api.view_user_costs'),
            headers=self.get_api_headers('bad-token', ''))
        self.assertTrue(response.status_code == 401)

        # get a token
        response = self.client.get(
            url_for('api.view_user_costs'),
            headers=self.get_api_headers('test@test.com', 'password'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the token
        response = self.client.get(
            url_for('api.view_user_costs'),
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)

    def test_unconfirmed_account(self):
        # add an unconfirmed user
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        db.session.add(u)
        db.session.commit()

        # get list of posts with the unconfirmed account
        response = self.client.get(
            url_for('api.view_user_costs'),
            headers=self.get_api_headers('test@test.com', 'password'))
        self.assertTrue(response.status_code == 403)

    def test_groups(self):
        # add a user
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        u.confirmed = True
        db.session.add(u)
        db.session.commit()

        # create invalid test group
        response = self.client.post(
            url_for('api.create_group'),
            headers=self.get_api_headers('test@test.com', 'password'),
            data=json.dumps({'name': ''}))
        self.assertTrue(response.status_code == 400)

        # create valid group
        response = self.client.post(
            url_for('api.create_group'),
            headers=self.get_api_headers('test@test.com', 'password'),
            data=json.dumps({'name': 'test_api'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('url')
        self.assertIsNotNone(url)

        # test response of creation group api
        response = self.client.get(
            url,
            headers=self.get_api_headers('test@test.com', 'password'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['name'] == 'test_api')
        json_group = json_response

        # create invalid memberships
        response = self.client.post(
            url_for('api.membership'),
            headers=self.get_api_headers('test@test.com', 'password'),
            data=json.dumps({'wrong': 1,
                             'group_id': 2}))
        self.assertTrue(response.status_code == 400)

        # create valid memberships
        response = self.client.post(
            url_for('api.create_group'),
            headers=self.get_api_headers('test@test.com', 'password'),
            data=json.dumps({'user_id': 1,
                             'group_id': 1}))
        self.assertTrue(response.status_code == 201)
