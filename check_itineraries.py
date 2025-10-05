#!/usr/bin/env python3
"""
Check itineraries in the database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from adminside.models import Package, Itinerary, ItineraryDay

print("Packages with itineraries:")
for package in Package.objects.filter(itinerary__isnull=False):
    days_count = package.itinerary.days.count()
    print(f"- {package.name}: {days_count} days")

print("\nItinerary details:")
for itinerary in Itinerary.objects.all():
    print(f"\n{itinerary.package.name}:")
    print(f"  Title: {itinerary.title}")
    print(f"  Overview: {itinerary.overview[:100]}...")
    print(f"  Days: {itinerary.days.count()}")

    for day in itinerary.days.all()[:2]:  # Show first 2 days
        print(f"    Day {day.day_number}: {day.title[:50]}...")