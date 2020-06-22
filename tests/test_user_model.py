from unittest import TestCase
from main_app import create_app, db
from main_app.models import User, Groups, Costs, CostGroup, Needs, Role, WhoOwesWhom, Permission, AnonUser
from config import Config
from time import sleep

class UserModelTestCase(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_role(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        self.assertEqual(u.role_id, 1)
        self.assertFalse(u.can(Permission.MODERATE))

    def test_moderator_role(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        u.role_id = 2
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_admin_role(self):
        u = User(username='username',
                 email=f'{Config.COSTAPP_ADMIN}',
                 password='password')
        self.assertEqual(u.role_id, 3)
        self.assertTrue(u.can(Permission.ADMIN))

    def test_password(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        self.assertTrue(u.password_hash is not None)
        self.assertTrue(u.check_password('password'))
        self.assertFalse(u.check_password('fake_password'))

    def test_password_hash(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        u2 = User(username='username1',
                  email='test1@test.com',
                  password='password1')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_confirmation_token(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        u2 = User(username='username1',
                  email='test1@test.com',
                  password='password1')
        db.session.add(u2)
        db.session.commit()
        self.assertFalse(u2.confirm(token))
        # test expiration confirmation token
        token = u2.generate_confirmation_token(expiration=1)
        sleep(2)
        self.assertFalse(u2.confirm(token))

    def test_anon_user(self):
        u = AnonUser()
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.COST))
        self.assertFalse(u.is_administrator())

    def test_to_json(self):
        u = User(username='username',
                 email='test@test.com',
                 password='password')
        db.session.add(u)
        db.session.commit()
        json_user = u.to_json()
        expected_keys = ['url', 'username', 'role', 'groups']
        self.assertEqual(sorted(json_user), sorted(expected_keys))
        self.assertTrue('api/users' in json_user['url'])




