from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile


CustomUser = get_user_model()

class ProfileSignalTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='signaluser@example.com',
            username='signaluser',
            password='testpass123'
        )

    def test_profile_created_on_user_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_profile_not_created_on_user_update(self):
        profile_count_before = Profile.objects.count()
        self.user.username = 'updateduser'
        self.user.save()
        profile_count_after = Profile.objects.count()
        self.assertEqual(profile_count_before, profile_count_after)

    def test_profile_defaults_after_creation(self):
        profile = self.user.profile
        self.assertEqual(profile.headline, '')
        self.assertIsNone(profile.bio)
        self.assertIsNone(profile.date_of_birth)
        self.assertEqual(profile.city, '')
        self.assertEqual(profile.country, '')
        self.assertFalse(profile.tech_stack.exists())
        self.assertIsNone(profile.contact_email)
        self.assertEqual(profile.languages, '')
        self.assertIsNone(profile.personal_website)
        self.assertIsNone(profile.linkedin)
        self.assertIsNone(profile.twitter)
        self.assertIsNone(profile.github)
        self.assertIsNone(profile.gitlab)
        self.assertFalse(profile.profile_picture)
