"""
    Sets config
"""

from django.apps import AppConfig


class BaseConfig(AppConfig):
    """Config for base module"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
