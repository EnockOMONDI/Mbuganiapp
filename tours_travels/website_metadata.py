"""Shared public metadata without invented reviews, prices or policy claims."""
import json
from urllib.parse import urlencode
from django.conf import settings

PAGES = {
 '/': ('Luxury safaris & thoughtful escapes', 'Discover Kenya and East Africa with Mbugani Luxe Adventures. Plan safaris, cultural journeys, beach escapes and group travel.'),
 '/aboutus/': ('Our story', 'Meet Mbugani Luxe Adventures and discover our approach to personal travel planning in Kenya and East Africa.'),
 '/services/': ('Travel services', 'Explore flight booking, hotels, safaris, conferences, group travel, team building, travel insurance and airport transfers.'),
 '/corporate/': ('Corporate travel', 'Plan business trips, conferences and corporate travel with Mbugani Luxe Adventures.'),
 '/holidays/': ('Holidays & escapes', 'Explore safari holidays and relaxing escapes with Mbugani Luxe Adventures.'),
 '/mice/': ('Meetings, incentives & events', 'Plan meetings, incentive travel, conferences and events with our travel team.'),
 '/student-travel/': ('Student & educational travel', 'Organise student trips and educational travel with Mbugani Luxe Adventures.'),
 '/ngo-travel/': ('NGO & humanitarian travel', 'Arrange travel for NGO teams, field operations and humanitarian programmes.'),
 '/contactus/': ('Contact our travel team', 'Contact Mbugani Luxe Adventures to plan your trip. Visit us at House of Leather or send an enquiry.'),
 '/quote/': ('Request a personal travel quote', 'Share your destination, dates and traveller count for a personal travel quote.'),
}


def website_metadata(request):
    name, description = PAGES.get(request.path, ('Explore with us', 'Explore travel experiences with Mbugani Luxe Adventures.'))
    origin = (getattr(settings, 'SITE_URL', '') or request.build_absolute_uri('/')).rstrip('/')
    canonical = origin + request.path
    page = request.GET.get('page', '')
    if page.isdigit() and int(page) > 1:
        canonical += '?' + urlencode({'page': page})
    organization = {'@context': 'https://schema.org', '@type': 'TravelAgency',
                    'name': 'Mbugani Luxe Adventures', 'url': origin,
                    'email': 'info@mbuganiluxeadventures.com', 'telephone': '+254701810167'}
    return {'default_page_title': name + ' | Mbugani Luxe Adventures',
            'default_meta_description': description, 'canonical_url': canonical,
            'organization_jsonld': json.dumps(organization).replace('<', '\\u003c'),
            'private_page': request.path.startswith(('/booking/', '/checkout/', '/profile/', '/account/', '/book/'))}
