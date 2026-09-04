from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Profile, Interest

User = get_user_model()

class UserAndProfileTests(TestCase):
    def test_create_user_successful(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # Profile should be auto-created
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.display_name, user.username)

    def test_create_superuser_successful(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="password123")
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_uniqueness(self):
        User.objects.create_user(email="dup@example.com", password="password123")
        with self.assertRaises(Exception):  # Should raise IntegrityError or similar DB exception
            User.objects.create_user(email="dup@example.com", password="anotherpassword")

    def test_profile_preferred_language_choices(self):
        user = User.objects.create_user(email="lang@example.com", password="password123")
        profile = user.profile
        profile.preferred_language = "ta"
        profile.save()
        self.assertEqual(profile.preferred_language, "ta")

        # Set to invalid language, full_clean() should raise ValidationError
        profile.preferred_language = "invalid"
        with self.assertRaises(ValidationError):
            profile.full_clean()

class InterestTests(TestCase):
    def setUp(self):
        self.interest_soil, _ = Interest.objects.get_or_create(name="Soil", defaults={'description': "Earth and soil health"})
        self.interest_yoga, _ = Interest.objects.get_or_create(name="Yoga", defaults={'description': "Meditation and physical yoga"})

    def test_interest_slug_auto_generation(self):
        self.assertEqual(self.interest_soil.slug, "soil")
        self.assertEqual(self.interest_yoga.slug, "yoga")

    def test_profile_interest_association(self):
        user = User.objects.create_user(email="interest_test@example.com", password="password123")
        profile = user.profile
        profile.interests.add(self.interest_soil, self.interest_yoga)
        
        self.assertEqual(profile.interests.count(), 2)
        self.assertIn(self.interest_soil, profile.interests.all())
        self.assertIn(self.interest_yoga, profile.interests.all())

class AccountViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password123")
        self.profile_url = reverse('accounts:profile')

    def test_profile_view_redirects_for_anonymous_user(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_profile_view_accessible_for_authenticated_user(self):
        self.client.login(email="user@example.com", password="password123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        
    def test_profile_update_successful(self):
        self.client.login(email="user@example.com", password="password123")
        interest, _ = Interest.objects.get_or_create(name="Soil")
        response = self.client.post(self.profile_url, {
            'display_name': 'New Display Name',
            'preferred_language': 'ta',
            'bio': 'New Bio description',
            'interests': [interest.id]
        })
        self.assertRedirects(response, self.profile_url)
        
        # Verify changes in DB
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.display_name, 'New Display Name')
        self.assertEqual(self.user.profile.preferred_language, 'ta')
        self.assertEqual(self.user.profile.bio, 'New Bio description')
        self.assertIn(interest, self.user.profile.interests.all())
