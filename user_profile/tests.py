from django.test import TestCase, LiveServerTestCase
from django.test import Client
import datetime
import time
# from django.utils import timezone
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse
from mod_drops.settings import STATIC_URL


import factory
import factory.django
from image.models import Image

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import os

# Test_File_Location = os.path.join(STATIC_URL, "Testimage.jpg")

TEST_DOMAIN_NAME = "http://127.0.0.1:8081"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: u'username%d' % n)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    title = factory.Sequence(lambda n: u'imagetitle%d' % n)
    user = factory.SubFactory(UserFactory)


class ImagerTestCase(TestCase):
    def setUp(self):
        bill = User(username='bill')
        sally = User(username='sally')
        bill.save()
        sally.save()

    def test_user(self):
        """Test  to see if user is being created."""
        bob = User(username='bob')
        alice = User(username='alice')
        bob.save()
        alice.save()
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(username='bob'), bob)
        self.assertEqual(User.objects.get(username='alice'), alice)

    def test_ImagerProfiles_Exist(self):
        """Test to see if creating a user creates UserProfile's"""
        bill = User.objects.get(username='bill')
        sally = User.objects.get(username='sally')
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(bill.profile.user, bill)
        self.assertEqual(sally.profile.user, sally)

    def test_is_active(self):
        """Test to see if we can see if a user is active from their profile"""
        bill = User.objects.get(username='bill')
        sally = User.objects.get(username='sally')
        self.assertTrue(bill.profile.is_active())
        self.assertTrue(sally.profile.is_active())
        bill.is_active = False
        bill.save()
        self.assertFalse(bill.profile.is_active())

    def test_active(self):
        """Test the active manager in UserProfile."""
        self.assertEqual(UserProfile.active.count(), 2)
        bill = User.objects.get(username='bill')
        bill.is_active = False
        bill.save()
        self.assertEqual(UserProfile.active.count(), 1)

    def test_unicode_and_str(self):
        """Test UserProfile to return unicode and str representations"""
        bill = User.objects.get(username='bill')
        bill_str = str(bill.profile)
        bill_unicode = unicode(bill.profile)
        self.assertTrue(isinstance(bill_str, str))
        self.assertTrue(isinstance(bill_unicode, unicode))


class ImagerFollowTestCase(TestCase):
    def setUp(self):
        self.bill = User(username='bill')
        self.sally = User(username='sally')
        self.tracy = User(username='tracy')
        self.bill.save()
        self.sally.save()
        self.tracy.save()

    def test_followers_empty(self):
        """ test to makes sure followers works on an empty set"""
        sally = self.sally.profile
        bill = self.bill.profile
        self.assertEqual(bill.followers.count(), 0)
        self.assertEqual(sally.followers.count(), 0)
        self.assertFalse(bool(bill.followers.all()))
        self.assertFalse(bool(sally.followers.all()))

    def test_following_empty(self):
        """ test to makes sure following works on an empty set"""
        sally = self.sally.profile
        bill = self.bill.profile
        self.assertEqual(bill.following.count(), 0)
        self.assertEqual(sally.following.count(), 0)

    def test_followers_query(self):
        """Tests to see if followers manager retrieves the right QuerySet
        Checks the case where two people follow a different person.
        """
        sally = self.sally.profile
        bill = self.bill.profile
        tracy = self.tracy.profile
        bill.follow(sally)
        tracy.follow(sally)
        # make sure both bill and tracy are followers of sally
        self.assertEqual(sally.followers.count(), 2)
        self.assertIn(bill, sally.followers.all())
        self.assertIn(tracy, sally.followers.all())
        # make sure followers is one way
        self.assertNotIn(sally, bill.followers.all())
        self.assertNotIn(sally, tracy.followers.all())
        self.assertEqual(bill.followers.count(), 0)
        self.assertEqual(tracy.followers.count(), 0)

    def test_following_query(self):
        """Tests to see if following manager retrieves the right QuerySet"""
        sally = self.sally.profile
        bill = self.bill.profile
        tracy = self.tracy.profile
        bill.follow(sally)
        bill.follow(tracy)
        # make sure  bill following both tracy and sally
        self.assertEqual(bill.following.count(), 2)
        self.assertIn(sally, bill.following.all())
        self.assertIn(tracy, bill.following.all())
        # make sure following is one way
        self.assertEqual(sally.following.count(), 0)
        self.assertEqual(tracy.following.count(), 0)
        self.assertNotIn(bill, tracy.following.all())
        self.assertNotIn(bill, sally.following.all())

    def test_follow(self):
        """Tests that follow works."""
        sally = self.sally.profile
        bill = self.bill.profile
        bill.follow(sally)
        self.assertEqual(bill.following.count(), 1)
        self.assertIn(sally, bill.following.all())
        self.assertEqual(sally.followers.count(), 1)
        self.assertIn(bill, sally.followers.all())

    def test_unfollow(self):
        """Tests that unfollow works."""
        sally = self.sally.profile
        bill = self.bill.profile
        bill.follow(sally)
        # unfollow and then make sure turned off on both sides
        bill.unfollow(sally)
        self.assertEqual(bill.following.count(), 0)
        self.assertNotIn(sally, bill.following.all())
        self.assertEqual(sally.followers.count(), 0)
        self.assertNotIn(bill, sally.followers.all())

    def test_unfollow_not_followed(self):
        """"Test that unfollow throws ValueError if that follow was not there"""
        sally = self.sally.profile
        bill = self.bill.profile
        with self.assertRaises(ValueError):
            bill.unfollow(sally)


class ImagerRegistration(TestCase):
    def setUp(self):
        self.user = {}
        self.user['bill'] = User.objects.create_user(username='bill',
                                                     password='secret')
        self.client1 = Client()

    def test_login_unauthorized(self):
        """Test that an unauthorized user cannot get in."""
        response = self.client1.post('/accounts/login/',
                                     {'username': 'hacker', 'password': 'badpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter a correct username and password.', response.content)
        is_logged_in = self.client1.login(username='hacker', password='badpass')
        self.assertFalse(is_logged_in)

    def test_login_authorized(self):
        """Test that an authorized user can get in."""
        response = self.client1.post('/accounts/login/',
                                     {'username': 'bill', 'password': 'secret'})
        self.assertEqual(response.status_code, 302)
        is_logged_in = self.client1.login(username='bill', password='secret')
        self.assertTrue(is_logged_in)


    def test_logout(self):
        """Test that an authorized user can log out."""
        is_logged_in = self.client1.login(username='bill', password='secret')
        self.assertTrue(is_logged_in)
        response = self.client1.post('/accounts/logout/')
        # Goes to an intermediate page that the user never sees before
        # going back to the home page
        self.assertIn('You are now logged out.', response.content)

    def test_library_security(self):
        pk = str(self.user['bill'].pk)
        response = self.client1.post('/image/library/')
        self.assertEqual(response.status_code, 302)

    def test_submitting_registration(self):
        response = self.client1.post('/accounts/register/',
                                     {'username': 'ted',
                                      'email': 'ted@ted.com',
                                      'password1': 'secret',
                                      'password2': 'secret'},
                                     follow=True)
        self.assertIn('/accounts/register/complete/', response.redirect_chain[0][0])
        self.assertEqual(response.status_code, 200)
        # make sure that user is created and they are not activated yet
        user1 = User.objects.get(username='ted')
        self.assertFalse(user1.is_active)

    def test_activate_with_good_key(self):
        response = self.client1.post('/accounts/register/',
                                     {'username': 'ted',
                                      'email': 'ted@ted.com',
                                      'password1': 'secret',
                                      'password2': 'secret'},
                                     follow=True)
        # user is not activate yet
        user1 = User.objects.get(username='ted')
        self.assertFalse(user1.is_active)
        activation_key = RegistrationProfile.objects.get(user=user1).activation_key
        activation_uri = reverse('registration_activate', kwargs={'activation_key': activation_key})
        response = self.client1.get(activation_uri, follow=True)
        user1 = User.objects.get(username='ted')
        # user is active after activating with key
        self.assertTrue(user1.is_active)

    def test_activation_with_wrong_key(self):
        response = self.client1.post('/accounts/register/',
                                     {'username': 'ted',
                                      'email': 'ted@ted.com',
                                      'password1': 'secret',
                                      'password2': 'secret'},
                                     follow=True)
        # user is not activate yet
        user1 = User.objects.get(username='ted')
        self.assertFalse(user1.is_active)
        activation_key = 'somepieceofcrap'
        activation_uri = reverse('registration_activate', kwargs={'activation_key': activation_key})
        response = self.client1.get(activation_uri, follow=True)
        user1 = User.objects.get(username='ted')
        # user is not active after activating with a bad key
        self.assertFalse(user1.is_active)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        # Setup a couple users with some content
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.save()
        self.user.profile.phone = 1234567
        self.user.profile.save()
        # self.profile = ImagerProfile(user=self.user, phone=1234567)
        # self.profile.save()

        self.another_user = User(username='user2')
        self.another_user.set_password('shall_not')
        self.another_user.save()
        self.another_user.profile.phone = 7654321
        self.another_user.profile.save()
        # self.another_profile = ImagerProfile(user=self.another_user, phone=7654321)
        # self.another_profile.save()

        self.photo1 = ImageFactory(user=self.user, published='PU')
        self.photo1.picture = 'something'
        self.photo1.save()
        self.photo2 = ImageFactory(user=self.user, published='PR')
        self.photo2.picture = 'else'
        self.photo2.save()

        self.client = Client()


    def test_user1_profile_view_self(self):
        # Login
        self.client.login(username='user1', password='pass')

        # Verify user1 sees his own information
        response = self.client.get(reverse('profile:profile'))
        self.assertIn(self.user.username, response.content)
        self.assertIn(str(self.user.profile.phone), response.content)

    def test_user1_profile_view_other(self):
        # Login
        self.client.login(username='user1', password='pass')

        # Verify user1 doesn't see user2's information
        response = self.client.get(reverse('profile:profile'))
        # user1 sees user1's info
        self.assertIn(self.user.username, response.content)
        self.assertIn(str(self.user.profile.phone), response.content)

        # But not user2's
        self.assertNotIn(self.another_user.username, response.content)
        self.assertNotIn(str(self.another_user.profile.phone), response.content)
