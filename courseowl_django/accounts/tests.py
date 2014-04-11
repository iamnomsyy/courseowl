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

    def login_with_password(self, password):
        """
        login as demo_user with various passwords
        on success: logs in and returns true
        on failure: returns false
        """
        return self.client.login(username='demo_user', password=password)

    def test_change_password(self):
        """
        Change password should succeed only if password == password_confirm
        Once password is changed, user shouldn't be able to log in with old password
        """

        # user can log in
        self.assertTrue(self.login_with_password('qwerty123'))

        # user changes password
        self.client.post('/accounts/change_password/', data={'password': '123qwerty', 'password_confirm': '123qwerty'})

        # user can log in with new password, but not the old
        self.assertFalse(self.login_with_password('qwerty123'))
        self.assertTrue(self.login_with_password('123qwerty'))

        # user changes password but fails confirm
        self.client.post('/accounts/change_password/', data={'password': 'abc123def', 'password_confirm': 'qwerty123'})

        # user didn't change password; can still log in with old password
        self.assertFalse(self.login_with_password('abc123def'))
        self.assertFalse(self.login_with_password('qwerty123'))
        self.assertTrue(self.login_with_password('123qwerty'))

    def test_change_email(self):
        """
        Change email should succeed only if the new email is not empty and another user does not have the same email
        """

        # user can log in:
        login_successful = self.client.login(username='demo_user', password='qwerty123')
        self.assertTrue(login_successful)

        # user changes email successfully:
        self.client.post('/accounts/change_email/', data={'new_email': 'demo_new@user.com'})

        temp_user = User.objects.get(email='demo_new@user.com')
        self.assertEqual('demo_new@user.com', temp_user.email)

        # user changes email to empty string, so it is not changed:
        self.client.post('/accounts/change_email/', data={'new_email': ''})
        self.assertEqual('demo_new@user.com', temp_user.email)

        # user changes email to invalid email, so it is not changed:
        self.client.post('/accounts/change_email/', data={'new_email': 'i like cats'})
        self.assertEqual('demo_new@user.com', temp_user.email)

        # user changes email to existing email, so it is not changed:
        second_user = User.objects.create_user(username='799b18ba74e7439a7fbd03c0c1e6da', email='second@abc.com', password='qwerty123', first_name='', last_name='')
        second_user.save()
        second_user_profile = UserProfile(user=second_user)
        second_user_profile.save()

        self.client.post('/accounts/change_email/', data={'new_email': 'second@abc.com'})
        self.assertEqual('demo_new@user.com', temp_user.email)

        # cleanup - change the email back to the original and delete the temporary second user
        self.client.post('/accounts/change_email/', data={'new_email': 'demo@user.com'})
        second_user.delete()

    def test_deactivate_account(self):
        login_successful = self.client.login(username='demo_user', password='qwerty123')
        self.assertTrue(login_successful)

        response = self.client.get('/accounts/deactivate_account/')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.login(username='demo_user', password='qwerty123'))  # make sure user cannot log in
