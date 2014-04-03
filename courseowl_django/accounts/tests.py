from django.test import TestCase
from django.test.client import Client

from accounts.views import *


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.demo_user = User.objects.create_user(username='demo_user', email='demo@user.com', password='qwerty123', first_name='', last_name='')
        self.demo_user.save()
        self.user_profile = UserProfile(user=self.demo_user)
        self.user_profile.save()

    def test_valid_email(self):
        email1 = 'testmail.cu'
        email2 = 'testmail%$#.com'
        email3 = 'test@#.com'
        email4 = 'test@mail.com'

        self.assertFalse(valid_email_address(email1))
        self.assertFalse(valid_email_address(email2))
        self.assertFalse(valid_email_address(email3))
        self.assertTrue(valid_email_address(email4))

    def test_valid_password(self):
        tooshort = 'short'
        blank = ''
        valid = 'qwerty123'

        short = check_valid_password(tooshort, tooshort)
        none = check_valid_password(blank, blank)
        notmatching1 = check_valid_password(tooshort, 'blah')
        notmatching2 = check_valid_password(blank, 'asdf')
        validpw = check_valid_password(valid, valid)

        self.assertFalse(short)
        self.assertFalse(none)
        self.assertFalse(notmatching1)
        self.assertFalse(notmatching2)
        self.assertTrue(validpw)

    def test_unique_user(self):
        email1 = 'test1@xyz.com'
        email2 = 'test2@xyz.com'
        password = 'qwerty123'
        user1 = User.objects.create_user(username_md5(email1), email1, password, first_name="", last_name="")

        user1_not_unique = unique_user(email1)
        user2_unique = unique_user(email2)
        self.assertFalse(user1_not_unique)
        self.assertTrue(user2_unique)

    def test_change_password(self):
        '''
        Change password should succeed only if password == password_confirm
        Once password is changed, user shouldn't be able to log in with old password
        '''

        # user can log in
        login_successful = self.client.login(username='demo_user', password='qwerty123')
        self.assertTrue(login_successful)

        # user changes password
        self.client.post('/accounts/change_password/', data={'password': '123qwerty', 'password_confirm': '123qwerty'})

        # user can log in with new password, but not the old
        login_successful = self.client.login(username='demo_user', password='qwerty123')
        self.assertFalse(login_successful)
        login_successful = self.client.login(username='demo_user', password='123qwerty')
        self.assertTrue(login_successful)

        # user changes password but fails confirm
        self.client.post('/accounts/change_password/', data={'password': 'abc123def', 'password_confirm': 'qwerty123'})

        # user didn't change password; can still log in with old password
        login_successful = self.client.login(username='demo_user', password='abc123def')
        self.assertFalse(login_successful)
        login_successful = self.client.login(username='demo_user', password='qwerty123')
        self.assertFalse(login_successful)
        login_successful = self.client.login(username='demo_user', password='123qwerty')
        self.assertTrue(login_successful)




