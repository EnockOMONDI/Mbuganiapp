#!/usr/bin/env python
"""
Script to add more comprehensive sample data including accommodations for all countries,
more travel packages, and blog content
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.contrib.auth.models import User
from adminside.models import Destination, Package, Accommodation, TravelMode, Itinerary, ItineraryDay
from blog.models import Category, Post

def add_more_accommodations():
    """Add accommodations for Tanzania, Rwanda, and Uganda"""
    print("Adding more accommodations...")
    
    # Get destinations
    tanzania = Destination.objects.get(slug="tanzania")
    arusha = Destination.objects.get(slug="arusha")
    serengeti = Destination.objects.get(slug="serengeti-national-park")
    
    rwanda = Destination.objects.get(slug="rwanda")
    kigali = Destination.objects.get(slug="kigali")
    volcanoes_np = Destination.objects.get(slug="volcanoes-national-park")
    
    uganda = Destination.objects.get(slug="uganda")
    kampala = Destination.objects.get(slug="kampala")
    bwindi = Destination.objects.get(slug="bwindi-impenetrable-forest")
    
    # Tanzania accommodations
    arusha_coffee_lodge = Accommodation.objects.create(
        name="Arusha Coffee Lodge",
        slug="arusha-coffee-lodge",
        accommodation_type=Accommodation.LODGE,
        description="""<p>Arusha Coffee Lodge is a boutique safari lodge set on one of Tanzania's largest coffee plantations. This unique property offers an authentic taste of Tanzanian coffee culture combined with luxury accommodations.</p>
        
        <p>Each plantation-style room is elegantly furnished and offers views of the coffee plantation and Mount Meru. The lodge provides an excellent base for exploring the northern Tanzania safari circuit.</p>""",
        destination=arusha,
        address="Arusha Coffee Plantation, Tanzania",
        price_per_room_per_night=380,
        max_occupancy_per_room=2,
        total_rooms=18,
        amenities="Coffee Plantation Tours, Restaurant, Bar, WiFi, Laundry Service, Airport Transfers, Cultural Activities",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.6'),
        total_reviews=156
    )
    
    serengeti_serena = Accommodation.objects.create(
        name="Serengeti Serena Safari Lodge",
        slug="serengeti-serena-safari-lodge",
        accommodation_type=Accommodation.LODGE,
        description="""<p>Serengeti Serena Safari Lodge is strategically positioned in the heart of the Serengeti, offering front-row seats to the Great Migration. The lodge's unique design blends seamlessly with the surrounding landscape.</p>
        
        <p>Built to resemble a traditional African village, the lodge offers comfortable accommodations with stunning views of the endless plains. Guests can enjoy exceptional game viewing right from the lodge.</p>""",
        destination=serengeti,
        address="Central Serengeti, Tanzania",
        price_per_room_per_night=520,
        max_occupancy_per_room=3,
        total_rooms=66,
        amenities="All Meals, Game Drives, Swimming Pool, Spa, Cultural Center, Gift Shop, Laundry Service",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.8'),
        total_reviews=203
    )
    
    # Rwanda accommodations
    kigali_serena = Accommodation.objects.create(
        name="Kigali Serena Hotel",
        slug="kigali-serena-hotel",
        accommodation_type=Accommodation.HOTEL,
        description="""<p>Kigali Serena Hotel is Rwanda's premier luxury hotel, located in the heart of Kigali with panoramic views over the city's rolling hills. This 5-star hotel offers world-class amenities and service.</p>
        
        <p>The hotel features elegantly appointed rooms, multiple dining options, conference facilities, and a fitness center. Its central location provides easy access to Kigali's business district and cultural attractions.</p>""",
        destination=kigali,
        address="KN 3 Ave, Kigali, Rwanda",
        price_per_room_per_night=280,
        max_occupancy_per_room=2,
        total_rooms=148,
        amenities="Free WiFi, Restaurant, Bar, Fitness Center, Spa, Conference Rooms, Business Center, Airport Shuttle",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.4'),
        total_reviews=187
    )
    
    mountain_gorilla_view = Accommodation.objects.create(
        name="Mountain Gorilla View Lodge",
        slug="mountain-gorilla-view-lodge",
        accommodation_type=Accommodation.LODGE,
        description="""<p>Mountain Gorilla View Lodge is perfectly positioned for gorilla trekking adventures in Volcanoes National Park. This eco-friendly lodge offers stunning views of the Virunga Mountains and comfortable accommodations.</p>
        
        <p>The lodge features stone cottages with fireplaces, a restaurant serving local and international cuisine, and a bar with panoramic mountain views. It's the ideal base for gorilla trekking and golden monkey tracking.</p>""",
        destination=volcanoes_np,
        address="Kinigi, Volcanoes National Park, Rwanda",
        price_per_room_per_night=420,
        max_occupancy_per_room=2,
        total_rooms=30,
        amenities="Gorilla Trekking Arrangements, Restaurant, Bar, Cultural Performances, Guided Nature Walks, Laundry Service",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.5'),
        total_reviews=142
    )
    
    # Uganda accommodations
    kampala_serena = Accommodation.objects.create(
        name="Kampala Serena Hotel",
        slug="kampala-serena-hotel",
        accommodation_type=Accommodation.HOTEL,
        description="""<p>Kampala Serena Hotel is Uganda's premier luxury hotel, located on Nakasero Hill with commanding views over the city and Lake Victoria. This 5-star hotel combines modern luxury with traditional Ugandan hospitality.</p>
        
        <p>The hotel offers elegantly furnished rooms, multiple dining venues, extensive conference facilities, and recreational amenities. Its prime location provides easy access to Kampala's business and cultural districts.</p>""",
        destination=kampala,
        address="Nakasero Hill, Kampala, Uganda",
        price_per_room_per_night=220,
        max_occupancy_per_room=2,
        total_rooms=152,
        amenities="Free WiFi, Multiple Restaurants, Bar, Fitness Center, Swimming Pool, Spa, Conference Facilities, Business Center",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.3'),
        total_reviews=198
    )
    
    bwindi_lodge = Accommodation.objects.create(
        name="Bwindi Lodge",
        slug="bwindi-lodge",
        accommodation_type=Accommodation.LODGE,
        description="""<p>Bwindi Lodge is an exclusive eco-lodge located on the edge of Bwindi Impenetrable Forest. This intimate lodge offers luxury accommodations in one of Africa's most pristine wilderness areas.</p>
        
        <p>The lodge features spacious bandas (traditional huts) with private verandas overlooking the forest. Guests enjoy gourmet meals, guided forest walks, and easy access to gorilla trekking starting points.</p>""",
        destination=bwindi,
        address="Bwindi Impenetrable Forest, Uganda",
        price_per_room_per_night=480,
        max_occupancy_per_room=2,
        total_rooms=8,
        amenities="Gorilla Trekking Permits, All Meals, Guided Forest Walks, Cultural Visits, Laundry Service, Airport Transfers",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.7'),
        total_reviews=89
    )
    
    print(f"Created {6} additional accommodations")

def add_more_travel_packages():
    """Add travel packages for Tanzania, Rwanda, and Uganda"""
    print("Adding more travel packages...")
    
    # Get destinations
    tanzania = Destination.objects.get(slug="tanzania")
    rwanda = Destination.objects.get(slug="rwanda")
    uganda = Destination.objects.get(slug="uganda")
    
    # Get accommodations
    serengeti_lodge = Accommodation.objects.get(slug="serengeti-serena-safari-lodge")
    arusha_lodge = Accommodation.objects.get(slug="arusha-coffee-lodge")
    
    gorilla_lodge = Accommodation.objects.get(slug="mountain-gorilla-view-lodge")
    kigali_hotel = Accommodation.objects.get(slug="kigali-serena-hotel")
    
    bwindi_lodge = Accommodation.objects.get(slug="bwindi-lodge")
    kampala_hotel = Accommodation.objects.get(slug="kampala-serena-hotel")
    
    # Tanzania Safari Package
    tanzania_safari = Package.objects.create(
        name="Tanzania Great Migration Safari",
        slug="tanzania-great-migration-safari",
        description="""<p>Witness one of nature's most spectacular events with this 8-day Tanzania Great Migration safari. Experience the dramatic river crossings and vast herds of wildebeest in the world-famous Serengeti ecosystem.</p>
        
        <p>This comprehensive safari includes the Serengeti National Park, Ngorongoro Crater, and Tarangire National Park. You'll stay in luxury lodges and enjoy expert guiding while experiencing the best wildlife viewing Tanzania has to offer.</p>
        
        <p>The timing of this safari is carefully planned to coincide with the Great Migration, ensuring you witness this incredible natural phenomenon. From dramatic river crossings to endless herds stretching to the horizon, this safari offers unforgettable memories.</p>""",
        main_destination=tanzania,
        duration_days=8,
        duration_nights=7,
        adult_price=3200,
        child_price=2560,
        inclusions="""<ul>
            <li>7 nights accommodation in luxury safari lodges</li>
            <li>All meals during the safari</li>
            <li>Professional English-speaking safari guide</li>
            <li>4WD safari vehicle with pop-up roof</li>
            <li>All park entrance fees</li>
            <li>Game drives in Serengeti, Ngorongoro, and Tarangire</li>
            <li>Ngorongoro Crater tour</li>
            <li>Airport transfers</li>
            <li>Bottled water during game drives</li>
            <li>Emergency evacuation insurance</li>
        </ul>""",
        exclusions="""<ul>
            <li>International flights</li>
            <li>Tanzania visa fees</li>
            <li>Travel insurance</li>
            <li>Personal expenses</li>
            <li>Alcoholic beverages</li>
            <li>Tips for guides and staff</li>
            <li>Optional activities</li>
        </ul>""",
        status=Package.PUBLISHED,
        is_featured=True,
        meta_title="Tanzania Great Migration Safari - 8 Days Serengeti & Ngorongoro",
        meta_description="Experience the Great Migration in Tanzania with this 8-day luxury safari. Serengeti, Ngorongoro Crater, and Tarangire National Park.",
        published_at=timezone.now()
    )
    
    tanzania_safari.available_accommodations.add(serengeti_lodge, arusha_lodge)
    
    print("Created Tanzania safari package")

if __name__ == "__main__":
    print("Adding more comprehensive sample data...")
    
    # Add more accommodations
    add_more_accommodations()
    
    # Add more travel packages
    add_more_travel_packages()
    
    print("Additional sample data completed!")
