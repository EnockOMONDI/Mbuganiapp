#!/usr/bin/env python
"""
Script to check the sample data in production database
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.contrib.auth.models import User
from adminside.models import Destination, Package, Accommodation
from blog.models import Category, Post

def check_production_data():
    print('Production Database Summary:')
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
        accommodations = Accommodation.objects.filter(destination__parent__parent=country).count()
        print(f'  {country.name}: {cities} cities, {places} places, {accommodations} accommodations')

    print('\nTravel Packages:')
    for package in Package.objects.all():
        accommodations_count = package.available_accommodations.count()
        print(f'  {package.name}')
        print(f'    Duration: {package.duration_days} days / {package.duration_nights} nights')
        print(f'    Price: ${package.adult_price} adult / ${package.child_price} child')
        print(f'    Accommodations: {accommodations_count}')
        print(f'    Status: {package.status}')
        print()

    print('Blog Categories:')
    for category in Category.objects.all():
        posts_count = category.post_set.count()
        print(f'  {category.title}: {posts_count} posts')

    print('\nBlog Posts:')
    for post in Post.objects.all():
        print(f'  {post.title} (Category: {post.category.title if post.category else "None"})')

if __name__ == "__main__":
    check_production_data()
