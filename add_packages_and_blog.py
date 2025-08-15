#!/usr/bin/env python
"""
Script to add Rwanda and Uganda packages, plus blog content
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
from adminside.models import Destination, Package, Accommodation
from blog.models import Category, Post

def add_rwanda_uganda_packages():
    """Add travel packages for Rwanda and Uganda"""
    print("Adding Rwanda and Uganda packages...")
    
    # Get destinations
    rwanda = Destination.objects.get(slug="rwanda")
    uganda = Destination.objects.get(slug="uganda")
    
    # Get accommodations
    gorilla_lodge = Accommodation.objects.get(slug="mountain-gorilla-view-lodge")
    kigali_hotel = Accommodation.objects.get(slug="kigali-serena-hotel")
    bwindi_lodge = Accommodation.objects.get(slug="bwindi-lodge")
    kampala_hotel = Accommodation.objects.get(slug="kampala-serena-hotel")
    
    # Rwanda Gorilla Trekking Package
    rwanda_gorillas = Package.objects.create(
        name="Rwanda Gorilla Trekking Experience",
        slug="rwanda-gorilla-trekking-experience",
        description="""<p>Embark on a life-changing adventure with this 4-day Rwanda gorilla trekking experience. Come face-to-face with mountain gorillas in their natural habitat in the pristine Volcanoes National Park.</p>
        
        <p>Rwanda offers one of the world's most exclusive wildlife experiences. With only a limited number of permits available daily, gorilla trekking in Rwanda is an intimate and unforgettable encounter with these magnificent creatures.</p>
        
        <p>This package includes comfortable accommodations, expert guides, and all necessary permits. You'll also have the opportunity to learn about Rwanda's remarkable conservation success story and visit local communities.</p>""",
        main_destination=rwanda,
        duration_days=4,
        duration_nights=3,
        adult_price=2800,
        child_price=2240,
        inclusions="""<ul>
            <li>3 nights accommodation in luxury lodge</li>
            <li>All meals during the stay</li>
            <li>Gorilla trekking permit (USD 1,500 value)</li>
            <li>Professional English-speaking guide</li>
            <li>4WD vehicle for transfers</li>
            <li>Kigali city tour</li>
            <li>Cultural village visit</li>
            <li>Airport transfers</li>
            <li>Bottled water</li>
            <li>Emergency evacuation insurance</li>
        </ul>""",
        exclusions="""<ul>
            <li>International flights</li>
            <li>Rwanda visa fees (USD 50)</li>
            <li>Travel insurance</li>
            <li>Personal expenses</li>
            <li>Alcoholic beverages</li>
            <li>Tips for guides and staff</li>
            <li>Optional activities</li>
            <li>Laundry services</li>
        </ul>""",
        status=Package.PUBLISHED,
        is_featured=True,
        meta_title="Rwanda Gorilla Trekking Experience - 4 Days Volcanoes National Park",
        meta_description="Experience mountain gorilla trekking in Rwanda's Volcanoes National Park. 4-day luxury package with permits included.",
        published_at=timezone.now()
    )
    
    rwanda_gorillas.available_accommodations.add(gorilla_lodge, kigali_hotel)
    
    # Uganda Gorilla and Wildlife Safari
    uganda_safari = Package.objects.create(
        name="Uganda Gorilla and Wildlife Safari",
        slug="uganda-gorilla-and-wildlife-safari",
        description="""<p>Discover the "Pearl of Africa" with this comprehensive 7-day Uganda safari combining gorilla trekking in Bwindi Impenetrable Forest with classic wildlife viewing in Queen Elizabeth National Park.</p>
        
        <p>Uganda offers incredible diversity - from mountain gorillas and chimpanzees to tree-climbing lions and boat safaris on the Kazinga Channel. This safari showcases the best of Uganda's wildlife and landscapes.</p>
        
        <p>Experience the thrill of tracking mountain gorillas through dense forest, enjoy game drives in search of the Big Five, and take a memorable boat safari while staying in comfortable accommodations throughout your journey.</p>""",
        main_destination=uganda,
        duration_days=7,
        duration_nights=6,
        adult_price=3400,
        child_price=2720,
        inclusions="""<ul>
            <li>6 nights accommodation in lodges and hotels</li>
            <li>All meals during the safari</li>
            <li>Gorilla trekking permit (USD 800 value)</li>
            <li>Professional English-speaking guide</li>
            <li>4WD safari vehicle</li>
            <li>Game drives in Queen Elizabeth National Park</li>
            <li>Boat safari on Kazinga Channel</li>
            <li>Chimpanzee tracking in Kibale Forest</li>
            <li>All park entrance fees</li>
            <li>Airport transfers</li>
            <li>Bottled water during activities</li>
        </ul>""",
        exclusions="""<ul>
            <li>International flights</li>
            <li>Uganda visa fees (USD 50)</li>
            <li>Travel insurance</li>
            <li>Personal expenses</li>
            <li>Alcoholic beverages</li>
            <li>Tips for guides and staff</li>
            <li>Optional activities</li>
            <li>Laundry services</li>
        </ul>""",
        status=Package.PUBLISHED,
        is_featured=True,
        meta_title="Uganda Gorilla and Wildlife Safari - 7 Days Bwindi & Queen Elizabeth",
        meta_description="Combine gorilla trekking with classic wildlife safari in Uganda. 7-day adventure through Bwindi Forest and Queen Elizabeth National Park.",
        published_at=timezone.now()
    )
    
    uganda_safari.available_accommodations.add(bwindi_lodge, kampala_hotel)
    
    print("Created Rwanda and Uganda packages")

def create_blog_categories():
    """Create blog categories"""
    print("Creating blog categories...")
    
    categories = [
        {
            'title': 'Safari Destinations',
            'slug': 'safari-destinations',
            'description': 'Explore the best safari destinations in East Africa'
        },
        {
            'title': 'Wildlife & Conservation',
            'slug': 'wildlife-conservation',
            'description': 'Learn about African wildlife and conservation efforts'
        },
        {
            'title': 'Travel Tips',
            'slug': 'travel-tips',
            'description': 'Essential tips for traveling in East Africa'
        },
        {
            'title': 'Cultural Experiences',
            'slug': 'cultural-experiences',
            'description': 'Discover the rich cultures of East Africa'
        },
        {
            'title': 'Adventure Activities',
            'slug': 'adventure-activities',
            'description': 'Thrilling adventures and activities in East Africa'
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'title': cat_data['title'],
                'description': cat_data['description'],
                'active': True
            }
        )
        created_categories.append(category)
    
    print(f"Created {len(created_categories)} blog categories")
    return created_categories

def create_blog_posts(categories):
    """Create sample blog posts"""
    print("Creating blog posts...")
    
    # Get the superuser
    user = User.objects.get(username='mbuganiluxeadventures')
    
    # Get categories
    safari_cat = next(cat for cat in categories if cat.slug == 'safari-destinations')
    wildlife_cat = next(cat for cat in categories if cat.slug == 'wildlife-conservation')
    tips_cat = next(cat for cat in categories if cat.slug == 'travel-tips')
    
    posts_data = [
        {
            'title': 'The Ultimate Guide to Kenya Safari: Maasai Mara vs Amboseli',
            'slug': 'ultimate-guide-kenya-safari-maasai-mara-vs-amboseli',
            'category': safari_cat,
            'excerpt': 'Discover the differences between Kenya\'s two most famous safari destinations and choose the perfect one for your African adventure.',
            'content': '''<p>Kenya offers some of the world's most spectacular safari experiences, with the Maasai Mara and Amboseli National Park standing out as the country's premier wildlife destinations. Each offers unique experiences and stunning wildlife viewing opportunities.</p>

<h2>Maasai Mara National Reserve</h2>
<p>The Maasai Mara is Kenya's most famous safari destination, renowned for the Great Migration and exceptional year-round wildlife viewing. From July to October, millions of wildebeest and zebras cross the Mara River, creating one of nature's most dramatic spectacles.</p>

<p>The reserve is home to an abundance of predators, including lions, leopards, and cheetahs. The open savanna grasslands provide excellent game viewing, and the Maasai people add a rich cultural dimension to any visit.</p>

<h2>Amboseli National Park</h2>
<p>Amboseli offers a completely different but equally rewarding experience. Famous for its large elephant herds and stunning views of Mount Kilimanjaro, Amboseli provides some of the most iconic African landscapes.</p>

<p>The park's diverse ecosystem includes wetlands, savanna, and woodlands, supporting a wide variety of wildlife. The elephants here are particularly well-studied and habituated, allowing for incredible close-up encounters.</p>

<h2>Which Should You Choose?</h2>
<p>Both destinations offer exceptional experiences. Choose Maasai Mara if you want to witness the Great Migration and see high concentrations of predators. Choose Amboseli for elephant encounters and Mount Kilimanjaro views. Better yet, visit both for the complete Kenya safari experience!</p>''',
            'tags': ['kenya', 'safari', 'maasai-mara', 'amboseli', 'wildlife'],
            'featured': True,
            'trending': True
        },
        {
            'title': 'Mountain Gorilla Conservation: A Success Story in Rwanda',
            'slug': 'mountain-gorilla-conservation-success-story-rwanda',
            'category': wildlife_cat,
            'excerpt': 'Learn how Rwanda transformed from tragedy to become a world leader in gorilla conservation and sustainable tourism.',
            'content': '''<p>Rwanda's mountain gorilla conservation program represents one of the most remarkable wildlife conservation success stories in Africa. From fewer than 250 individuals in the 1980s, the mountain gorilla population has steadily increased thanks to dedicated conservation efforts.</p>

<h2>The Conservation Challenge</h2>
<p>Mountain gorillas face numerous threats including habitat loss, poaching, and human encroachment. These magnificent creatures are found only in the Virunga Mountains, shared between Rwanda, Uganda, and the Democratic Republic of Congo.</p>

<p>Rwanda's approach to conservation has been comprehensive, involving local communities, international partnerships, and sustainable tourism. The country has invested heavily in anti-poaching efforts, habitat protection, and community development.</p>

<h2>Community Involvement</h2>
<p>One of the key factors in Rwanda's success has been involving local communities in conservation efforts. Revenue from gorilla tourism is shared with communities, providing economic incentives for conservation.</p>

<p>Local people are employed as guides, trackers, and in various tourism-related businesses. This creates a direct link between conservation success and community prosperity.</p>

<h2>The Future</h2>
<p>Today, Rwanda's mountain gorilla population continues to grow, and the country serves as a model for conservation efforts across Africa. Visitors to Rwanda not only experience incredible wildlife encounters but also contribute directly to conservation efforts.</p>''',
            'tags': ['rwanda', 'gorillas', 'conservation', 'wildlife', 'sustainability'],
            'featured': True,
            'trending': False
        }
    ]
    
    created_posts = []
    for post_data in posts_data:
        post = Post.objects.create(
            user=user,
            title=post_data['title'],
            slug=post_data['slug'],
            excerpt=post_data['excerpt'],
            content=post_data['content'],
            category=post_data['category'],
            status='published',
            featured=post_data['featured'],
            trending=post_data['trending']
        )
        
        # Add tags
        post.tags.add(*post_data['tags'])
        created_posts.append(post)
    
    print(f"Created {len(created_posts)} blog posts")
    return created_posts

if __name__ == "__main__":
    print("Adding packages and blog content...")
    
    # Add Rwanda and Uganda packages
    add_rwanda_uganda_packages()
    
    # Create blog categories
    categories = create_blog_categories()
    
    # Create blog posts
    posts = create_blog_posts(categories)
    
    print("Packages and blog content completed!")
