"""
    Category and Subscription models
"""

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Model for handling Category in the database"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name.__str__()


class Subscription(models.Model):
    """Model for handling Subscription in the database"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    provider = models.CharField(max_length=200)
    service = models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} {self.service}"
