"""
    Handles the GET and POST requests
"""
# pylint: disable=E1101
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

import matplotlib.pyplot as plt
import numpy as np

from base.forms import SubscriptionForm
from base.models import Subscription, Category


def login_page(request):
    """Handles the logic of the login page"""
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Username OR password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    """Logs out the user"""
    logout(request)
    return redirect('home')


def register_user(request):
    """Handles the logic of the registration process"""
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    """Logic of the search bar listing, querying"""
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    subscriptions = Subscription.objects.filter(
        Q(category__name__icontains=query) |
        Q(provider__icontains=query) |
        Q(service__icontains=query)
    )

    categories = Category.objects.all()
    subscriptions_count = subscriptions.count()

    context = {'subscriptions': subscriptions, 'categories': categories,
               'subscriptions_count': subscriptions_count}
    return render(request, 'base/home.html', context)


def subscription(request, key):
    """Logic for presenting the subscription"""
    subscription_obj = Subscription.objects.get(id=key)
    if request.user != subscription_obj.owner:
        return redirect('home')
    context = {'subscription': subscription_obj}
    return render(request, 'base/subscription.html', context)


@login_required(login_url='login')
def create_subscription(request):
    """Handles presenting and processing the create form"""
    form = SubscriptionForm()
    form.fields["owner"].initial = request.user
    form.fields["owner"].disabled = True
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get_or_create(id=int(category_id))[0]

        Subscription.objects.create(
            owner=request.user,
            category=category,
            provider=request.POST.get('provider'),
            service=request.POST.get('service'),
            price=request.POST.get('price'),
        )
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/subscription_form.html', context)


@login_required(login_url='login')
def update_subscription(request, key):
    """Handles presenting and processing the update form"""
    subscription_obj = Subscription.objects.get(id=key)
    form = SubscriptionForm(instance=subscription_obj)
    form.fields["owner"].disabled = True
    if request.user != subscription_obj.owner:
        return redirect('home')

    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get_or_create(id=int(category_id))[0]
        subscription_obj.provider = request.POST.get('provider')
        subscription_obj.service = request.POST.get('service')
        subscription_obj.category = category
        subscription_obj.price = request.POST.get('price')
        subscription_obj.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/subscription_form.html', context)


@login_required(login_url='login')
def delete_subscription(request, key):
    """Handles presenting and processing the delete form"""
    subscription_obj = Subscription.objects.get(id=key)
    if request.user != subscription_obj.owner:
        return redirect('home')

    if request.method == 'POST':
        subscription_obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': subscription_obj})


def stats(request):
    """Handles presenting and calculating the stats"""
    subscriptions = Subscription.objects.filter(owner=request.user)
    total_sum = 0
    stats_obj = {}
    for subscription_obj in subscriptions:
        previous_value = stats_obj.get(subscription_obj.category, 0)
        stats_obj[subscription_obj.category] =\
            previous_value + subscription_obj.price
        total_sum += subscription_obj.price

    stat_keys = []
    stat_values = []
    for key, value in stats_obj.items():
        stat_keys.append(key)
        stat_values.append(value)

    plt.pie(np.array(stat_values), labels=stat_keys)

    plt.savefig('base/static/piechart.png')
    plt.close()
    context = {'total_sum': total_sum, 'stats': stats_obj}

    return render(request, 'base/stats.html', context=context)
