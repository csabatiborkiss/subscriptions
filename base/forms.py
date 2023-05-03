"""
    The form for handling CRUD of subscriptions
"""

from django.forms import ModelForm
from .models import Subscription


class SubscriptionForm(ModelForm):
    """Model form for subscriptions"""
    class Meta:
        """Metadata for SubscriptionForm"""
        model = Subscription
        fields = '__all__'
