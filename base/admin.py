"""
Registers the models to the django admin site
"""

from django.contrib import admin

from base.models import Subscription, Category

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Category)
