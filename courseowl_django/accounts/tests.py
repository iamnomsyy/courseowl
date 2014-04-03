from django.test import TestCase
from django.test.client import Client
from accounts.views import *


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bob12345', email='bob@bob.com', password='bob123456', first_name='', last_name='')
        self.user.save()
        self.user_profile = UserProfile(user=self.user)
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

    def test_deactivate_account(self):
        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        response = self.client.get('/accounts/deactivate_account/')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.login(username='bob12345', password='bob123456'))  # make sure user cannot log in
