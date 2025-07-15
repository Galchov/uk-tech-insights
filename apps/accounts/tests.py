from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Profile
from apps.technologies.models import Technology


CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='TestUser@Example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_email_is_lowercase(self):
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_is_verified_default(self):
        self.assertFalse(self.user.is_verified)

    def test_user_fields(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'is_verified'))

    def test_save_lowercase_on_update(self):
        self.user.email = 'NewEmail@Example.COM'
        self.user.save()
        self.assertEqual(self.user.email, 'newemail@example.com')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='profileuser@example.com',
            username='profileuser',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_profile_str(self):
        self.assertEqual(str(self.profile), f"Profile of {self.user.username}")

    def test_profile_creation_defaults(self):
        self.assertEqual(self.profile.headline, '')
        self.assertIsNone(self.profile.bio)
        self.assertIsNone(self.profile.date_of_birth)
        self.assertEqual(self.profile.city, '')
        self.assertEqual(self.profile.country, '')
        self.assertFalse(self.profile.tech_stack.exists())
        self.assertIsNone(self.profile.contact_email)
        self.assertEqual(self.profile.languages, '')
        self.assertIsNone(self.profile.personal_website)
        self.assertIsNone(self.profile.linkedin)
        self.assertIsNone(self.profile.twitter)
        self.assertIsNone(self.profile.github)
        self.assertIsNone(self.profile.gitlab)
        self.assertFalse(self.profile.profile_picture)

    def test_profile_tech_stack(self):
        tech1 = Technology.objects.create(name='Python')
        tech2 = Technology.objects.create(name='Django')

        self.profile.tech_stack.add(tech1, tech2)
        self.assertIn(tech1, self.profile.tech_stack.all())
        self.assertIn(tech2, self.profile.tech_stack.all())
