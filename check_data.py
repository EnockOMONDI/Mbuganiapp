#!/usr/bin/env python
"""
Script to check the sample data in development database
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.contrib.auth.models import User
from adminside.models import Destination, Package, Accommodation
from blog.models import Category, Post

def check_data():
    print('Development Database Summary:')
    print(f'Users: {User.objects.count()}')
    print(f'Destinations: {Destination.objects.count()}')
    print(f'  - Countries: {Destination.objects.filter(destination_type="country").count()}')
    print(f'  - Cities: {Destination.objects.filter(destination_type="city").count()}')
    print(f'  - Places: {Destination.objects.filter(destination_type="place").count()}')
    print(f'Accommodations: {Accommodation.objects.count()}')
    print(f'Travel Packages: {Package.objects.count()}')
    print(f'Blog Categories: {Category.objects.count()}')
    print(f'Blog Posts: {Post.objects.count()}')

    print('\nDestinations by Country:')
    for country in Destination.objects.filter(destination_type='country'):
        cities = country.children.filter(destination_type='city').count()
        places = Destination.objects.filter(parent__parent=country, destination_type='place').count()
        print(f'  {country.name}: {cities} cities, {places} places')

    print('\nTravel Packages:')
    for package in Package.objects.all():
        print(f'  {package.name} - {package.duration_days} days - ${package.adult_price}')

if __name__ == "__main__":
    check_data()
