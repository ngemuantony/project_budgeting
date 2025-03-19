from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import StaffUserProfile, EndUserProfile


class UsersManagersTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        # Test creation of a regular user
        user = self.User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.type, self.User.Types.ENDUSER)

        # Verify EndUserProfile creation
        self.assertTrue(EndUserProfile.objects.filter(user=user).exists())

        # Check username behavior
        with self.assertRaises(AttributeError):
            _ = user.username

        # Test missing parameters
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email="", password="foo")

    def test_create_staff_user(self):
        # Test creation of a staff user
        user = self.User.objects.create_user(
            email="staff@user.com", password="foo", type=self.User.Types.STAFF
        )
        self.assertEqual(user.email, "staff@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.type, self.User.Types.STAFF)

        # Verify StaffUserProfile creation
        self.assertTrue(StaffUserProfile.objects.filter(user=user).exists())

    def test_create_superuser(self):
        # Test creation of a superuser
        admin_user = self.User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.type, self.User.Types.STAFF)

        # Verify no profiles are created for superuser
        self.assertFalse(StaffUserProfile.objects.filter(user=admin_user).exists())
        self.assertFalse(EndUserProfile.objects.filter(user=admin_user).exists())

        # Test invalid superuser creation
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

    def test_email_normalization(self):
        # Test email normalization
        user = self.User.objects.create_user(email="NORMAL@USER.COM", password="foo")
        self.assertEqual(user.email, "normal@user.com")

    def test_type_field(self):
        # Test setting the type field
        staff_user = self.User.objects.create_user(
            email="staff@user.com", password="foo", type=self.User.Types.STAFF
        )
        self.assertEqual(staff_user.type, self.User.Types.STAFF)

        end_user = self.User.objects.create_user(
            email="enduser@user.com", password="foo", type=self.User.Types.ENDUSER
        )
        self.assertEqual(end_user.type, self.User.Types.ENDUSER)

    def test_profile_creation_on_save(self):
        # Test profile creation based on type
        staff_user = self.User.objects.create_user(
            email="staff@user.com", password="foo", type=self.User.Types.STAFF
        )
        self.assertTrue(StaffUserProfile.objects.filter(user=staff_user).exists())
        self.assertFalse(EndUserProfile.objects.filter(user=staff_user).exists())

        end_user = self.User.objects.create_user(
            email="enduser@user.com", password="foo", type=self.User.Types.ENDUSER
        )
        self.assertTrue(EndUserProfile.objects.filter(user=end_user).exists())
        self.assertFalse(StaffUserProfile.objects.filter(user=end_user).exists())