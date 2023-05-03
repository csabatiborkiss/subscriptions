from django.test import TestCase
from base.models import Subscription, Category
from django.contrib.auth.models import User
"""Unit tests get placed here"""


class SubscriptionTestCase(TestCase):
    def setUp(self):
        mock_user = User()
        mock_user.save()
        mock_category = Category(name="CategoryName")
        mock_category.save()
        Subscription.objects.create(owner=mock_user, category=mock_category,
                                    provider="SubProv", service="SubService",
                                    price=100)

    def test_subscriptions(self):
        test_sub = Subscription.objects.get(provider="SubProv")
        self.assertEqual(test_sub.provider, "SubProv", "Subscription provider error")
        self.assertEqual(test_sub.service, "SubService", "Subscription service error")
        self.assertEqual(test_sub.price, 100, "Subscription price error")
        self.assertEqual(test_sub.category.name, "CategoryName", "Subscription Category name error")
        self.assertIsInstance(test_sub.owner, User, "Subscription owner error")


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="CategoryName")

    def test_categories(self):
        test_category = Category.objects.get(name="CategoryName")
        self.assertEqual(test_category.name, "CategoryName", "Category name error")
