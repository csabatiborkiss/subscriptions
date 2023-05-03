"""
    Defines possible routings in the app
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('', views.home, name='home'),
    path('subscription/<str:key>/', views.subscription, name='subscription'),
    path('create-subscription/', views.create_subscription,
         name='create-subscription'),
    path('update-subscription/<str:key>/', views.update_subscription,
         name='update-subscription'),
    path('delete-subscription/<str:key>/', views.delete_subscription,
         name='delete-subscription'),
    path('statistics/', views.stats, name='statistics'),
    re_path(r'.*', views.home)
]
