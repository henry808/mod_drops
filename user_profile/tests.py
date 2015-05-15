from django.test import TestCase, LiveServerTestCase
from django.test import Client
import datetime
import time
# from django.utils import timezone
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse
from mod_drops.settings import STATIC_URL, STATIC_ROOT


import factory
import factory.django
from image.models import Image

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

Test_File_Location = os.path.join(STATIC_ROOT, "user_profile/images/Testimage.jpg")

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


# class ImagerTestCase(TestCase):
#     def setUp(self):
#         bill = User(username='bill')
#         sally = User(username='sally')
#         bill.save()
#         sally.save()

#     def test_user(self):
#         """Test  to see if user is being created."""
#         bob = User(username='bob')
#         alice = User(username='alice')
#         bob.save()
#         alice.save()
#         self.assertEqual(User.objects.count(), 4)
#         self.assertEqual(User.objects.get(username='bob'), bob)
#         self.assertEqual(User.objects.get(username='alice'), alice)

#     def test_ImagerProfiles_Exist(self):
#         """Test to see if creating a user creates UserProfile's"""
#         bill = User.objects.get(username='bill')
#         sally = User.objects.get(username='sally')
#         self.assertEqual(UserProfile.objects.count(), 2)
#         self.assertEqual(bill.profile.user, bill)
#         self.assertEqual(sally.profile.user, sally)

#     def test_is_active(self):
#         """Test to see if we can see if a user is active from their profile"""
#         bill = User.objects.get(username='bill')
#         sally = User.objects.get(username='sally')
#         self.assertTrue(bill.profile.is_active())
#         self.assertTrue(sally.profile.is_active())
#         bill.is_active = False
#         bill.save()
#         self.assertFalse(bill.profile.is_active())

#     def test_active(self):
#         """Test the active manager in UserProfile."""
#         self.assertEqual(UserProfile.active.count(), 2)
#         bill = User.objects.get(username='bill')
#         bill.is_active = False
#         bill.save()
#         self.assertEqual(UserProfile.active.count(), 1)

#     def test_unicode_and_str(self):
#         """Test UserProfile to return unicode and str representations"""
#         bill = User.objects.get(username='bill')
#         bill_str = str(bill.profile)
#         bill_unicode = unicode(bill.profile)
#         self.assertTrue(isinstance(bill_str, str))
#         self.assertTrue(isinstance(bill_unicode, unicode))


# class ImagerFollowTestCase(TestCase):
#     def setUp(self):
#         self.bill = User(username='bill')
#         self.sally = User(username='sally')
#         self.tracy = User(username='tracy')
#         self.bill.save()
#         self.sally.save()
#         self.tracy.save()

#     def test_followers_empty(self):
#         """ test to makes sure followers works on an empty set"""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         self.assertEqual(bill.followers.count(), 0)
#         self.assertEqual(sally.followers.count(), 0)
#         self.assertFalse(bool(bill.followers.all()))
#         self.assertFalse(bool(sally.followers.all()))

#     def test_following_empty(self):
#         """ test to makes sure following works on an empty set"""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         self.assertEqual(bill.following.count(), 0)
#         self.assertEqual(sally.following.count(), 0)

#     def test_followers_query(self):
#         """Tests to see if followers manager retrieves the right QuerySet
#         Checks the case where two people follow a different person.
#         """
#         sally = self.sally.profile
#         bill = self.bill.profile
#         tracy = self.tracy.profile
#         bill.follow(sally)
#         tracy.follow(sally)
#         # make sure both bill and tracy are followers of sally
#         self.assertEqual(sally.followers.count(), 2)
#         self.assertIn(bill, sally.followers.all())
#         self.assertIn(tracy, sally.followers.all())
#         # make sure followers is one way
#         self.assertNotIn(sally, bill.followers.all())
#         self.assertNotIn(sally, tracy.followers.all())
#         self.assertEqual(bill.followers.count(), 0)
#         self.assertEqual(tracy.followers.count(), 0)

#     def test_following_query(self):
#         """Tests to see if following manager retrieves the right QuerySet"""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         tracy = self.tracy.profile
#         bill.follow(sally)
#         bill.follow(tracy)
#         # make sure  bill following both tracy and sally
#         self.assertEqual(bill.following.count(), 2)
#         self.assertIn(sally, bill.following.all())
#         self.assertIn(tracy, bill.following.all())
#         # make sure following is one way
#         self.assertEqual(sally.following.count(), 0)
#         self.assertEqual(tracy.following.count(), 0)
#         self.assertNotIn(bill, tracy.following.all())
#         self.assertNotIn(bill, sally.following.all())

#     def test_follow(self):
#         """Tests that follow works."""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         bill.follow(sally)
#         self.assertEqual(bill.following.count(), 1)
#         self.assertIn(sally, bill.following.all())
#         self.assertEqual(sally.followers.count(), 1)
#         self.assertIn(bill, sally.followers.all())

#     def test_unfollow(self):
#         """Tests that unfollow works."""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         bill.follow(sally)
#         # unfollow and then make sure turned off on both sides
#         bill.unfollow(sally)
#         self.assertEqual(bill.following.count(), 0)
#         self.assertNotIn(sally, bill.following.all())
#         self.assertEqual(sally.followers.count(), 0)
#         self.assertNotIn(bill, sally.followers.all())

#     def test_unfollow_not_followed(self):
#         """"Test that unfollow throws ValueError if that follow was not there"""
#         sally = self.sally.profile
#         bill = self.bill.profile
#         with self.assertRaises(ValueError):
#             bill.unfollow(sally)


# class ImagerRegistration(TestCase):
#     def setUp(self):
#         self.user = {}
#         self.user['bill'] = User.objects.create_user(username='bill',
#                                                      password='secret')
#         self.client1 = Client()

#     def test_login_unauthorized(self):
#         """Test that an unauthorized user cannot get in."""
#         response = self.client1.post('/accounts/login/',
#                                      {'username': 'hacker', 'password': 'badpass'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Please enter a correct username and password.', response.content)
#         is_logged_in = self.client1.login(username='hacker', password='badpass')
#         self.assertFalse(is_logged_in)

#     def test_login_authorized(self):
#         """Test that an authorized user can get in."""
#         response = self.client1.post('/accounts/login/',
#                                      {'username': 'bill', 'password': 'secret'})
#         self.assertEqual(response.status_code, 302)
#         is_logged_in = self.client1.login(username='bill', password='secret')
#         self.assertTrue(is_logged_in)


#     def test_logout(self):
#         """Test that an authorized user can log out."""
#         is_logged_in = self.client1.login(username='bill', password='secret')
#         self.assertTrue(is_logged_in)
#         response = self.client1.post('/accounts/logout/')
#         # Goes to an intermediate page that the user never sees before
#         # going back to the home page
#         self.assertIn('You are now logged out.', response.content)

#     def test_library_security(self):
#         pk = str(self.user['bill'].pk)
#         response = self.client1.post('/image/library/')
#         self.assertEqual(response.status_code, 302)

#     def test_submitting_registration(self):
#         response = self.client1.post('/accounts/register/',
#                                      {'username': 'ted',
#                                       'email': 'ted@ted.com',
#                                       'password1': 'secret',
#                                       'password2': 'secret'},
#                                      follow=True)
#         self.assertIn('/accounts/register/complete/', response.redirect_chain[0][0])
#         self.assertEqual(response.status_code, 200)
#         # make sure that user is created and they are not activated yet
#         user1 = User.objects.get(username='ted')
#         self.assertFalse(user1.is_active)

#     def test_activate_with_good_key(self):
#         response = self.client1.post('/accounts/register/',
#                                      {'username': 'ted',
#                                       'email': 'ted@ted.com',
#                                       'password1': 'secret',
#                                       'password2': 'secret'},
#                                      follow=True)
#         # user is not activate yet
#         user1 = User.objects.get(username='ted')
#         self.assertFalse(user1.is_active)
#         activation_key = RegistrationProfile.objects.get(user=user1).activation_key
#         activation_uri = reverse('registration_activate', kwargs={'activation_key': activation_key})
#         response = self.client1.get(activation_uri, follow=True)
#         user1 = User.objects.get(username='ted')
#         # user is active after activating with key
#         self.assertTrue(user1.is_active)

#     def test_activation_with_wrong_key(self):
#         response = self.client1.post('/accounts/register/',
#                                      {'username': 'ted',
#                                       'email': 'ted@ted.com',
#                                       'password1': 'secret',
#                                       'password2': 'secret'},
#                                      follow=True)
#         # user is not activate yet
#         user1 = User.objects.get(username='ted')
#         self.assertFalse(user1.is_active)
#         activation_key = 'somepieceofcrap'
#         activation_uri = reverse('registration_activate', kwargs={'activation_key': activation_key})
#         response = self.client1.get(activation_uri, follow=True)
#         user1 = User.objects.get(username='ted')
#         # user is not active after activating with a bad key
#         self.assertFalse(user1.is_active)


# class UserProfileViewTestCase(TestCase):
#     def setUp(self):
#         # Setup a couple users with some content
#         self.user = User(username='user1')
#         self.user.set_password('pass')
#         self.user.save()
#         self.user.profile.phone = 1234567
#         self.user.profile.save()

#         self.another_user = User(username='user2')
#         self.another_user.set_password('shall_not')
#         self.another_user.save()
#         self.another_user.profile.phone = 7654321
#         self.another_user.profile.phone_privacy = 'PU'
#         self.another_user.profile.save()


#         self.photo1 = ImageFactory(user=self.user, published='PU')
#         self.photo1.picture = 'something'
#         self.photo1.save()
#         self.photo2 = ImageFactory(user=self.user, published='PR')
#         self.photo2.picture = 'else'
#         self.photo2.save()

#         self.client = Client()


#     def test_user1_profile_view_self(self):
#         """See self in profile view"""
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 sees his own information
#         response = self.client.get(reverse('profile:profile'))
#         self.assertIn(self.user.username, response.content)
#         self.assertIn(str(self.user.profile.phone), response.content)

#     def test_user1_profile_view_other(self):
#         """Don't see other in profile view"""
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 doesn't see user2's information
#         response = self.client.get(reverse('profile:profile'))
#         # user1 sees user1's info
#         self.assertIn(self.user.username, response.content)
#         self.assertIn(str(self.user.profile.phone), response.content)

#         # But not user2's
#         self.assertNotIn(self.another_user.username, response.content)
#         self.assertNotIn(str(self.another_user.profile.phone), response.content)

#     def test_user1_profile_other_view(self):
#         """See other in other profile view"""
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 doesn't see user2's information
#         response = self.client.get(
#             reverse('profile:other_profile',
#                     kwargs={'pk': self.another_user.profile.pk}))
#         # user1 sees user2's info
#         self.assertIn(self.another_user.username, response.content)
#         # make sure phone that was set to public is displayed
#         self.assertIn(str(self.another_user.profile.phone), response.content)


# class UserProfileUpdateTestCase(TestCase):
#     def setUp(self):
#         # Setup a couple users with some content
#         self.users = {}
#         self.users['user1'] = User(username='user1')
#         self.users['user1'].set_password('pass')
#         self.users['user1'].save()
#         self.users['user1'].profile.phone = 1234567
#         self.users['user1'].profile.save()


#         self.users['user2'] = User(username='user2')
#         self.users['user2'].set_password('shall_not')
#         self.users['user2'].save()
#         self.users['user2'].profile.phone = 7654321
#         self.users['user2'].profile.save()


#         self.photo1 = ImageFactory(user=self.users['user1'], published='PU')
#         self.photo1.picture = 'something'
#         self.photo1.save()
#         self.photo2 = ImageFactory(user=self.users['user1'], published='PR')
#         self.photo2.picture = 'else'
#         self.photo2.save()

#         self.client = Client()

#     def test_user1_profile_update_view_self(self):
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 sees his own information
#         response = self.client.get(reverse('profile:profile_update', kwargs={'pk': self.users['user1'].profile.pk}))
#         self.assertIn(self.users['user1'].username, response.content)
#         self.assertIn(str(self.users['user1'].profile.phone), response.content)


#     def test_user1_profile_view_other(self):
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 doesn't see user2's information
#         response = self.client.get(reverse('profile:profile_update', kwargs={'pk': self.users['user1'].profile.pk}))
#         # user1 sees user1's info
#         self.assertIn(self.users['user1'].username, response.content)
#         self.assertIn(str(self.users['user1'].profile.phone), response.content)

#         # But not user2's
#         self.assertNotIn(self.users['user2'].username, response.content)
#         self.assertNotIn(str(self.users['user2'].profile.phone), response.content)


#     def test_user1_profile_update_view_complete_data(self):
#         # Login
#         self.client.login(username='user1', password='pass')

#         # Verify user1 sees his own information
#         response = self.client.get(reverse('profile:profile_update', kwargs={'pk': self.users['user1'].profile.pk}))
#         # make sure reponse it OK
#         self.assertEquals(response.status_code, 200)
#         # Verify user1 sees his own information
#         self.assertIn(self.users['user1'].username, response.content)
#         self.assertIn(str(self.users['user1'].profile.phone), response.content)

#         # post form data
#         response = self.client.post(
#             reverse('profile:profile_update', kwargs={'pk': self.users['user1'].profile.pk}),
#             {'phone': 678,
#              'first_name': 'Jim',
#              'last_name': 'Gordon',
#              'name_privacy': 'PR',
#              'email_privacy': 'PR',
#              'phone_privacy': 'PR',
#              'birthday_privacy': 'PR',
#              'pic_privacy': 'PR',
#              'email': 'user1@user1.com',
#              'birthday': '1980-03-15'
#              }, follow=True)
#         self.users['user1'] = User.objects.get(id=self.users['user1'].id)
#         # Changes to User
#         self.assertEquals(self.users['user1'].first_name, 'Jim')
#         self.assertEquals(self.users['user1'].last_name, 'Gordon')
#         self.assertEquals(self.users['user1'].email, 'user1@user1.com')
#         # Changes to ImagerProfile
#         self.assertEquals(self.users['user1'].profile.phone, '678')
#         self.assertEquals(self.users['user1'].profile.birthday,
#                           datetime.date(1980, 3, 15))
#         # Goes back to profile view after
#         self.assertIn('Profile Detail View', response.content)


class UserProfileDetailTestCase(LiveServerTestCase):
    """This class is for testing user login form, and profile form"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(UserProfileDetailTestCase, self).setUp
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.is_active = True

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
        super(UserProfileDetailTestCase, self).tearDown()

    def test_goto_homepage(self):
        self.driver.get(self.live_server_url)
        self.assertIn("Home", self.driver.title)

    def login_user(self):
        """login user"""
        self.driver.get(TEST_DOMAIN_NAME + reverse('auth_login'))
        username_field = self.driver.find_element_by_id('id_username')
        username_field.send_keys('user1')
        password_field = self.driver.find_element_by_id('id_password')
        password_field.send_keys('pass')
        form = self.driver.find_element_by_tag_name('form')
        form.submit()


    def test_login(self):
        self.user.save()
        self.login_user()
        self.assertIn("Home", self.driver.title)
        self.assertIn("user1", self.driver.page_source)

    def test_profile_populates(self):
        self.user.first_name = "user_first"
        self.user.last_name = "user_last"
        self.user.email = "email@email.com"
        self.user.save()
        self.user.profile.phone = 1234
        self.user.profile.birthday = datetime.date(1980, 3, 15)
        self.user.profile.pic_privacy = 'PU'
        self.user.profile.birthday_privacy = 'PR'
        self.user.profile.phone_privacy = 'PU'
        self.user.profile.name_privacy = 'PR'
        self.user.profile.email_privacy = 'PR'
        self.user.profile.save()
        self.login_user()
        link = self.driver.find_element_by_link_text(str(self.user.username))
        link.click()
        self.assertIn("Profile Detail View", self.driver.page_source)
        link = self.driver.find_element_by_link_text('Edit')
        link.click()
        # Profile page: see if user info is populated
        info_list = [('id_email', self.user.email),
                     ('id_first_name', self.user.first_name),
                     ('id_last_name', self.user.last_name)]
        for info in info_list:
            field = self.driver.find_element_by_id(info[0])
            self.assertIn(str(info[1]), field.get_attribute('value'))
        # Profile page: see if profile info is populated
        info_list = [('id_phone', self.user.profile.phone),
                     ('id_birthday', self.user.profile.birthday),
                     ('id_pic_privacy', self.user.profile.pic_privacy),
                     ('id_birthday_privacy', self.user.profile.birthday_privacy),
                     ('id_phone_privacy', self.user.profile.phone_privacy),
                     ('id_name_privacy', self.user.profile.name_privacy),
                     ('id_email_privacy', self.user.profile.email_privacy),
                     ('id_picture', self.user.profile.picture.name)]
        for info in info_list:
            field = self.driver.find_element_by_id(info[0])
            if info[0] == 'id_picture':
                pass
                # no name defined because using default photo
                # self.assertIn(str(info[1]), self.driver.page_source)
            else:
                self.assertIn(str(info[1]), field.get_attribute('value'))

    def test_profile_form_saves(self):
        """Test to make sure all data in a filled out form saves properly"""
        self.user.save()
        self.login_user()
        link = self.driver.find_element_by_link_text(str(self.user.username))
        link.click()
        self.assertIn("Profile Detail View", self.driver.page_source)
        link = self.driver.find_element_by_link_text('Edit')
        link.click()
        first_name = 'new_first_name'
        last_name = 'new_last_name'
        email = 'newem@email.com'
        phone = '999'
        date = "4/14/1970"
        public = 'PU'

        # Profile page: Fill Out User Info
        info_list = [('id_email', email),
                     ('id_first_name', first_name),
                     ('id_last_name', last_name)]
        for info in info_list:
            field = self.driver.find_element_by_id(info[0])
            field.send_keys(info[1])
        # Profile page: Fill Out Profile Info
        info_list = [('id_phone', phone),
                     ('id_birthday', date),
                     ('id_picture', Test_File_Location),
                     ('id_pic_privacy', public),
                     ('id_birthday_privacy', public),
                     ('id_phone_privacy', public),
                     ('id_name_privacy', public),
                     ('id_email_privacy', public)]
        for info in info_list:
            field = self.driver.find_element_by_id(info[0])
            if info[0] == 'id_birthday':
                field.clear()
            field.send_keys(info[1])
        form = self.driver.find_element_by_tag_name('form')
        form.submit()

        # Check if info is in the profile view
        self.driver.implicitly_wait(4)
        self.assertIn("Profile Detail View", self.driver.page_source)
        self.user = User.objects.get(username=self.user.username)
        check_inputs = [(self.user.first_name, first_name),
                        (self.user.last_name, last_name),
                        (self.user.email, email),
                        (self.user.profile.phone, phone),
                        (self.user.profile.birthday,  datetime.date(1970, 4, 14)),
                        (self.user.profile.pic_privacy, public),
                        (self.user.profile.birthday_privacy, public),
                        (self.user.profile.phone_privacy, public),
                        (self.user.profile.name_privacy, public),
                        (self.user.profile.email_privacy, public)]

        for field in check_inputs:
            self.assertEquals(field[0], field[1])
        self.assertIn("Testimage", self.user.profile.picture.name)


# class BadUser(LiveServerTestCase):
#     """ Make sure that other user can't do things they should
#         not be able to.
#     """
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.user = User(username='user1')
#         self.user.set_password('password1')
#         self.user.save()
#         self.user.profile.phone = 1234567
#         self.user.profile.save()

#     def tearDown(self):
#         self.driver.implicitly_wait(4)
#         self.driver.quit()

#     def test_profile_redirect(self):
#         self.driver.get(self.live_server_url + reverse('profile:profile'))
#         self.assertIn('Log in', self.driver.page_source)
#         self.driver.get(self.live_server_url + reverse('profile:profile'))
#         self.assertIn('Log in', self.driver.page_source)

#     def test_upload_photo_redirect(self):
#         self.driver.get(self.live_server_url + reverse('image:upload_image'))
#         self.assertIn('Log in', self.driver.page_source)

#     def test_edit_photo_hack(self):
#         photo = ImageFactory(user=self.user, published='PR')
#         photo.picture = 'else'
#         photo.save()

#         other = User(username='user2')
#         other.set_password('password2')
#         other.save()
#         other.profile.phone = 7654321
#         other.profile.save()

#         self.login('user2', 'password2')

#         self.driver.get(self.live_server_url + reverse('image:edit_image', kwargs={'pk': photo.pk}))
#         self.assertIn('Log in', self.driver.page_source)

#     def test_edit_album_redirect(self):
#         self.driver.get(self.live_server_url + reverse('image:library'))
#         self.assertIn('Log in', self.driver.page_source)


#     def test_bad_login_redirect(self):
#         self.driver.get(self.live_server_url + reverse('auth_login'))
#         self.driver.find_element_by_id('id_username').send_keys('hi')
#         self.driver.find_element_by_id('id_password').send_keys('wrong')
#         self.driver.find_element_by_tag_name('form').submit()

#     def login(self, user, password):
#         self.driver.get(self.live_server_url + reverse('auth_login'))
#         namefield = self.driver.find_element_by_id('id_username').send_keys(user)
#         passfield = self.driver.find_element_by_id('id_password').send_keys(password)
