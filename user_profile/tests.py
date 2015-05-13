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
        self.assertEqual(bill.profile.is_active, True)
        self.assertEqual(sally.profile.is_active, True)
        bill.is_active = False
        bill.save()
        self.assertEqual(bill.profile.is_active, False)

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
        self.assertEqual(isinstance(bill_str, str), True)
        self.assertEqual(isinstance(bill_unicode, unicode), True)

