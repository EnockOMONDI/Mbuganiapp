#!/usr/bin/env python
"""
Script to populate the development database with comprehensive sample travel data
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.contrib.auth.models import User
from adminside.models import Destination, Package, Accommodation, TravelMode, Itinerary, ItineraryDay
from blog.models import Category, Post

def create_destinations():
    """Create destination hierarchy: Countries -> Cities -> Places"""
    print("Creating destinations...")
    
    # Countries
    kenya = Destination.objects.create(
        name="Kenya",
        slug="kenya",
        destination_type=Destination.COUNTRY,
        description="""<p>Kenya is a country in East Africa renowned for its diverse landscapes, abundant wildlife, and rich cultural heritage. From the iconic savannas of the Maasai Mara to the pristine beaches of the Indian Ocean coast, Kenya offers unforgettable experiences for every traveler.</p>
        
        <p>The country is home to the Great Migration, one of nature's most spectacular events, where millions of wildebeest and zebras cross the Mara River. Kenya's national parks and reserves protect an incredible array of wildlife including the Big Five: lions, elephants, buffalo, leopards, and rhinos.</p>
        
        <p>Beyond wildlife, Kenya boasts vibrant cultures, with over 40 different ethnic groups, each with unique traditions, languages, and customs. The warm hospitality of the Kenyan people, combined with the country's natural beauty, makes it a premier safari destination in Africa.</p>""",
        is_featured=True,
        is_active=True,
        display_order=1
    )
    
    tanzania = Destination.objects.create(
        name="Tanzania",
        slug="tanzania",
        destination_type=Destination.COUNTRY,
        description="""<p>Tanzania is home to some of Africa's most famous national parks and natural wonders. The country encompasses the legendary Serengeti National Park, the magnificent Ngorongoro Crater, and Africa's highest peak, Mount Kilimanjaro.</p>
        
        <p>The Serengeti ecosystem hosts the Great Migration, where over two million wildebeest, zebras, and gazelles move in an endless cycle of life. Tanzania's diverse landscapes range from vast savannas and volcanic highlands to tropical coastlines along the Indian Ocean.</p>
        
        <p>The country is also rich in cultural diversity, with over 120 ethnic groups living harmoniously. From the Maasai warriors of the northern plains to the Swahili culture of the coast, Tanzania offers authentic cultural experiences alongside world-class wildlife viewing.</p>""",
        is_featured=True,
        is_active=True,
        display_order=2
    )
    
    rwanda = Destination.objects.create(
        name="Rwanda",
        slug="rwanda",
        destination_type=Destination.COUNTRY,
        description="""<p>Rwanda, known as the "Land of a Thousand Hills," is a small but remarkable country in East Africa. Despite its tragic history, Rwanda has emerged as one of Africa's most progressive and safest destinations, offering unique wildlife experiences and stunning landscapes.</p>
        
        <p>The country is world-famous for mountain gorilla trekking in Volcanoes National Park, where visitors can encounter these magnificent creatures in their natural habitat. Rwanda's commitment to conservation has made it a model for sustainable tourism in Africa.</p>
        
        <p>Beyond gorillas, Rwanda offers beautiful lakes, rolling hills, and vibrant culture. The capital, Kigali, is one of Africa's cleanest and most organized cities, serving as a gateway to the country's natural wonders.</p>""",
        is_featured=True,
        is_active=True,
        display_order=3
    )
    
    uganda = Destination.objects.create(
        name="Uganda",
        slug="uganda",
        destination_type=Destination.COUNTRY,
        description="""<p>Uganda, the "Pearl of Africa," is a landlocked country blessed with incredible biodiversity, stunning landscapes, and warm, welcoming people. From the source of the Nile River to the snow-capped Rwenzori Mountains, Uganda offers diverse experiences for adventurous travelers.</p>
        
        <p>The country is renowned for its primate experiences, including mountain gorilla trekking in Bwindi Impenetrable Forest and chimpanzee tracking in Kibale Forest. Uganda is home to over half of the world's remaining mountain gorillas, making it a premier destination for wildlife enthusiasts.</p>
        
        <p>Uganda's landscapes are incredibly varied, featuring tropical rainforests, vast savannas, crater lakes, and the mighty Nile River. The country's rich cultural heritage includes over 50 different ethnic groups, each contributing to Uganda's vibrant tapestry of traditions and customs.</p>""",
        is_featured=True,
        is_active=True,
        display_order=4
    )
    
    return kenya, tanzania, rwanda, uganda

def create_cities_and_places(countries):
    """Create cities and places for each country"""
    print("Creating cities and places...")
    
    kenya, tanzania, rwanda, uganda = countries
    destinations = {}
    
    # Kenya cities and places
    nairobi = Destination.objects.create(
        name="Nairobi",
        slug="nairobi",
        destination_type=Destination.CITY,
        description="""<p>Nairobi, Kenya's vibrant capital city, is a unique blend of urban sophistication and wild nature. Known as the "Green City in the Sun," Nairobi serves as the gateway to Kenya's incredible safari destinations while offering its own attractions.</p>
        
        <p>The city is home to Nairobi National Park, the only national park in the world located within a capital city, where visitors can see lions, rhinos, and giraffes against the backdrop of city skyscrapers. The David Sheldrick Wildlife Trust and Giraffe Centre offer intimate wildlife encounters and conservation education.</p>""",
        parent=kenya,
        is_featured=True,
        is_active=True,
        display_order=1
    )
    
    maasai_mara = Destination.objects.create(
        name="Maasai Mara",
        slug="maasai-mara",
        destination_type=Destination.PLACE,
        description="""<p>The Maasai Mara National Reserve is Kenya's most famous safari destination and one of Africa's greatest wildlife reserves. This vast expanse of savanna grassland is home to an incredible concentration of wildlife and hosts the spectacular Great Migration.</p>
        
        <p>From July to October, millions of wildebeest, zebras, and gazelles cross the Mara River from Tanzania's Serengeti, creating one of nature's most dramatic spectacles. The reserve is also home to the Big Five and offers excellent opportunities to see lions, leopards, elephants, buffalo, and rhinos.</p>""",
        parent=nairobi,
        is_featured=True,
        is_active=True,
        display_order=1
    )
    
    amboseli = Destination.objects.create(
        name="Amboseli National Park",
        slug="amboseli-national-park",
        destination_type=Destination.PLACE,
        description="""<p>Amboseli National Park offers some of the best views of Mount Kilimanjaro and is famous for its large herds of elephants. The park's diverse ecosystem includes wetlands, savanna, and woodlands, supporting a wide variety of wildlife.</p>
        
        <p>The park is particularly renowned for its elephant research and conservation efforts. Visitors can observe these magnificent creatures up close while enjoying the stunning backdrop of Africa's highest mountain.</p>""",
        parent=nairobi,
        is_featured=True,
        is_active=True,
        display_order=2
    )
    
    destinations['kenya'] = {
        'country': kenya,
        'cities': [nairobi],
        'places': [maasai_mara, amboseli]
    }

    # Tanzania cities and places
    arusha = Destination.objects.create(
        name="Arusha",
        slug="arusha",
        destination_type=Destination.CITY,
        description="""<p>Arusha is Tanzania's safari capital and the gateway to the country's most famous national parks. Located at the foot of Mount Meru, this bustling city serves as the starting point for most northern Tanzania safari circuits.</p>

        <p>The city offers a perfect blend of African culture and modern amenities, with vibrant markets, cultural heritage sites, and excellent restaurants. Arusha is also home to the East African Community headquarters and serves as a major conference destination.</p>""",
        parent=tanzania,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    serengeti = Destination.objects.create(
        name="Serengeti National Park",
        slug="serengeti-national-park",
        destination_type=Destination.PLACE,
        description="""<p>The Serengeti National Park is Tanzania's oldest and most popular national park, famous for the annual Great Migration. This vast ecosystem covers 14,750 square kilometers of endless plains, making it larger than Connecticut.</p>

        <p>The park is home to over 2 million wildebeest, 200,000 zebras, and 300,000 Thomson's gazelles. The Serengeti also boasts the largest population of lions in Africa and offers exceptional game viewing year-round.</p>""",
        parent=arusha,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    kilimanjaro = Destination.objects.create(
        name="Mount Kilimanjaro",
        slug="mount-kilimanjaro",
        destination_type=Destination.PLACE,
        description="""<p>Mount Kilimanjaro, Africa's highest peak at 5,895 meters, is a dormant volcano and one of the world's most iconic mountains. Known as the "Roof of Africa," Kilimanjaro attracts climbers from around the globe seeking to reach its summit, Uhuru Peak.</p>

        <p>The mountain features three volcanic cones and five distinct climate zones, from tropical rainforest at the base to arctic conditions at the summit. The climb typically takes 5-9 days and offers breathtaking views and diverse ecosystems.</p>""",
        parent=arusha,
        is_featured=True,
        is_active=True,
        display_order=2
    )

    destinations['tanzania'] = {
        'country': tanzania,
        'cities': [arusha],
        'places': [serengeti, kilimanjaro]
    }

    # Rwanda cities and places
    kigali = Destination.objects.create(
        name="Kigali",
        slug="kigali",
        destination_type=Destination.CITY,
        description="""<p>Kigali, Rwanda's capital and largest city, is renowned as one of Africa's cleanest and safest cities. Built on rolling hills, Kigali offers stunning views and a well-organized urban environment that reflects Rwanda's remarkable transformation.</p>

        <p>The city serves as the country's economic and cultural hub, featuring modern infrastructure, excellent restaurants, and important historical sites including the Kigali Genocide Memorial. Kigali is the perfect base for exploring Rwanda's natural wonders.</p>""",
        parent=rwanda,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    volcanoes_np = Destination.objects.create(
        name="Volcanoes National Park",
        slug="volcanoes-national-park",
        destination_type=Destination.PLACE,
        description="""<p>Volcanoes National Park is Rwanda's premier destination for mountain gorilla trekking. Located in the Virunga Mountains, this park protects the Rwandan portion of the Virunga Massif, home to several habituated gorilla families.</p>

        <p>The park covers 160 square kilometers of rainforest and bamboo forest, providing habitat for mountain gorillas, golden monkeys, and over 200 bird species. Gorilla trekking here offers an intimate and life-changing wildlife experience.</p>""",
        parent=kigali,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    nyungwe = Destination.objects.create(
        name="Nyungwe Forest National Park",
        slug="nyungwe-forest-national-park",
        destination_type=Destination.PLACE,
        description="""<p>Nyungwe Forest National Park is one of Africa's oldest rainforests and Rwanda's largest protected area. This pristine montane rainforest is home to 13 primate species, including chimpanzees and colobus monkeys.</p>

        <p>The park features an impressive canopy walkway, offering visitors a unique perspective of the forest from 50 meters above the ground. Nyungwe is also a birder's paradise with over 300 bird species recorded.</p>""",
        parent=kigali,
        is_featured=True,
        is_active=True,
        display_order=2
    )

    destinations['rwanda'] = {
        'country': rwanda,
        'cities': [kigali],
        'places': [volcanoes_np, nyungwe]
    }

    # Uganda cities and places
    kampala = Destination.objects.create(
        name="Kampala",
        slug="kampala",
        destination_type=Destination.CITY,
        description="""<p>Kampala, Uganda's vibrant capital, is built on seven hills and serves as the country's political, economic, and cultural center. The city offers a fascinating blend of traditional African culture and modern urban life.</p>

        <p>Key attractions include the Kasubi Tombs (a UNESCO World Heritage Site), bustling markets, and the source of the Nile at Jinja nearby. Kampala provides an excellent introduction to Ugandan culture and serves as the gateway to the country's national parks.</p>""",
        parent=uganda,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    bwindi = Destination.objects.create(
        name="Bwindi Impenetrable Forest",
        slug="bwindi-impenetrable-forest",
        destination_type=Destination.PLACE,
        description="""<p>Bwindi Impenetrable Forest National Park is Uganda's premier gorilla trekking destination and a UNESCO World Heritage Site. This ancient rainforest is home to almost half of the world's remaining mountain gorillas.</p>

        <p>The park's dense, misty forest covers 331 square kilometers and harbors an incredible diversity of flora and fauna. Besides gorillas, Bwindi is home to over 120 mammal species and 350 bird species, making it one of Africa's most biodiverse forests.</p>""",
        parent=kampala,
        is_featured=True,
        is_active=True,
        display_order=1
    )

    queen_elizabeth = Destination.objects.create(
        name="Queen Elizabeth National Park",
        slug="queen-elizabeth-national-park",
        destination_type=Destination.PLACE,
        description="""<p>Queen Elizabeth National Park is Uganda's most popular savanna park and a UNESCO Biosphere Reserve. The park offers diverse ecosystems including savanna, wetlands, lowland forest, and crater lakes.</p>

        <p>Famous for its tree-climbing lions in the Ishasha sector and boat safaris on the Kazinga Channel, the park is home to over 95 mammal species and 600 bird species. The dramatic backdrop of the Rwenzori Mountains adds to the park's spectacular scenery.</p>""",
        parent=kampala,
        is_featured=True,
        is_active=True,
        display_order=2
    )

    destinations['uganda'] = {
        'country': uganda,
        'cities': [kampala],
        'places': [bwindi, queen_elizabeth]
    }

    return destinations

def create_accommodations(destinations):
    """Create sample accommodations for each destination"""
    print("Creating accommodations...")

    accommodations = {}

    # Kenya accommodations
    # Nairobi accommodations
    nairobi_serena = Accommodation.objects.create(
        name="Nairobi Serena Hotel",
        slug="nairobi-serena-hotel",
        accommodation_type=Accommodation.HOTEL,
        description="""<p>The Nairobi Serena Hotel is a luxury 5-star hotel located in the heart of Nairobi's business district. This elegant hotel combines modern amenities with traditional African hospitality, offering guests a sophisticated urban retreat.</p>

        <p>The hotel features beautifully appointed rooms and suites, multiple dining options, a fitness center, and conference facilities. Its central location provides easy access to Nairobi's attractions, shopping centers, and business districts.</p>""",
        destination=destinations['kenya']['cities'][0],  # Nairobi
        address="Kenyatta Avenue, Nairobi, Kenya",
        price_per_room_per_night=250,
        max_occupancy_per_room=2,
        total_rooms=183,
        amenities="Free WiFi, Restaurant, Bar, Fitness Center, Conference Rooms, 24-hour Room Service, Laundry Service, Airport Shuttle",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.5'),
        total_reviews=245
    )

    # Maasai Mara accommodations
    mara_serena_lodge = Accommodation.objects.create(
        name="Mara Serena Safari Lodge",
        slug="mara-serena-safari-lodge",
        accommodation_type=Accommodation.LODGE,
        description="""<p>Mara Serena Safari Lodge is perched high on a hill overlooking the vast plains of the Maasai Mara. This award-winning lodge offers panoramic views of the reserve and provides an authentic safari experience with luxury amenities.</p>

        <p>The lodge features traditional Maasai-inspired architecture and décor, with comfortable rooms offering stunning views. Guests can enjoy game drives, cultural visits to Maasai villages, and world-class dining while experiencing the Great Migration.</p>""",
        destination=destinations['kenya']['places'][0],  # Maasai Mara
        address="Maasai Mara National Reserve, Kenya",
        price_per_room_per_night=450,
        max_occupancy_per_room=3,
        total_rooms=74,
        amenities="All Meals Included, Game Drives, Cultural Visits, Swimming Pool, Spa, Gift Shop, Laundry Service",
        is_active=True,
        is_featured=True,
        rating=Decimal('4.7'),
        total_reviews=189
    )

    accommodations['kenya'] = [nairobi_serena, mara_serena_lodge]

    return accommodations

def create_travel_packages(destinations, accommodations):
    """Create comprehensive travel packages"""
    print("Creating travel packages...")

    packages = []

    # Get the superuser for package creation
    user = User.objects.get(username='mbuganiluxeadventures')

    # Kenya Safari Package
    kenya_safari = Package.objects.create(
        name="Ultimate Kenya Safari Adventure",
        slug="ultimate-kenya-safari-adventure",
        description="""<p>Experience the best of Kenya with this comprehensive 7-day safari adventure that takes you through the country's most iconic destinations. Witness the Great Migration in the Maasai Mara and enjoy close encounters with elephants against the backdrop of Mount Kilimanjaro in Amboseli.</p>

        <p>This carefully crafted itinerary combines thrilling game drives, cultural experiences with the Maasai people, and comfortable accommodations. You'll have the opportunity to see the Big Five and experience one of nature's greatest spectacles - the annual wildebeest migration.</p>

        <p>Our expert guides will ensure you have the best wildlife viewing opportunities while learning about Kenya's diverse ecosystems and conservation efforts. This safari is perfect for first-time visitors to Africa and seasoned travelers alike.</p>""",
        main_destination=destinations['kenya']['country'],
        duration_days=7,
        duration_nights=6,
        adult_price=2850,
        child_price=2280,
        inclusions="""<ul>
            <li>6 nights accommodation in luxury safari lodges</li>
            <li>All meals during the safari (breakfast, lunch, dinner)</li>
            <li>Professional English-speaking safari guide</li>
            <li>4WD safari vehicle with pop-up roof for game viewing</li>
            <li>All park entrance fees and conservancy fees</li>
            <li>Game drives in Maasai Mara and Amboseli National Parks</li>
            <li>Cultural visit to a traditional Maasai village</li>
            <li>Airport transfers in Nairobi</li>
            <li>Bottled water during game drives</li>
            <li>Emergency evacuation insurance</li>
        </ul>""",
        exclusions="""<ul>
            <li>International flights to/from Kenya</li>
            <li>Kenya visa fees (USD 50 for most nationalities)</li>
            <li>Travel insurance (highly recommended)</li>
            <li>Personal expenses and souvenirs</li>
            <li>Alcoholic beverages and soft drinks</li>
            <li>Tips for guides and lodge staff</li>
            <li>Optional activities not mentioned in the itinerary</li>
            <li>Laundry services</li>
        </ul>""",
        status=Package.PUBLISHED,
        is_featured=True,
        meta_title="Ultimate Kenya Safari Adventure - 7 Days Maasai Mara & Amboseli",
        meta_description="Experience Kenya's best wildlife destinations on this 7-day safari adventure. See the Great Migration, Big Five, and enjoy luxury accommodations.",
        published_at=datetime.now()
    )

    # Add accommodations to the package
    kenya_safari.available_accommodations.add(*accommodations['kenya'])

    packages.append(kenya_safari)

    return packages

if __name__ == "__main__":
    print("Starting sample data population...")

    # Create destinations
    countries = create_destinations()
    destinations = create_cities_and_places(countries)

    # Create accommodations
    accommodations = create_accommodations(destinations)

    # Create travel packages
    packages = create_travel_packages(destinations, accommodations)

    print("Sample data population completed!")
