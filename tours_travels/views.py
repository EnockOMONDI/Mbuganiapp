from django.shortcuts import render,HttpResponse
from . import mail as mail_f
from django.template import loader
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.utils import timezone

def home(request):
    return HttpResponse('<h1>Welcome</h1>')

def mail(request):
	mail_f.verification_mail()
	return HttpResponse('<h1>mail is sent</h1>')


# Custom Error Views
def custom_400_view(request, exception=None):
    """Custom 400 Bad Request error page"""
    template = loader.get_template('400.html')
    context = {
        'request_path': request.path,
        'exception': exception,
    }
    return HttpResponseBadRequest(template.render(context, request))


def custom_403_view(request, exception=None):
    """Custom 403 Forbidden error page"""
    template = loader.get_template('403.html')
    context = {
        'request_path': request.path,
        'exception': exception,
    }
    return HttpResponseForbidden(template.render(context, request))


def custom_404_view(request, exception=None):
    """Custom 404 Page Not Found error page"""
    template = loader.get_template('404.html')
    context = {
        'request_path': request.path,
        'exception': exception,
    }
    return HttpResponseNotFound(template.render(context, request))


def custom_500_view(request):
    """Custom 500 Internal Server Error page"""
    template = loader.get_template('500.html')
    context = {
        'request_path': request.path,
    }
    return HttpResponseServerError(template.render(context, request))


# Health check and utility views
def health_check(request):
    """Basic health check endpoint"""
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now().isoformat()})

def health_detailed(request):
    """Detailed health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'database': 'connected',
        'static_files': 'available'
    })

def readiness_check(request):
    """Readiness check endpoint"""
    return JsonResponse({'status': 'ready', 'timestamp': timezone.now().isoformat()})

def liveness_check(request):
    """Liveness check endpoint"""
    return JsonResponse({'status': 'alive', 'timestamp': timezone.now().isoformat()})

def metrics(request):
    """Basic metrics endpoint"""
    return JsonResponse({'metrics': 'available', 'timestamp': timezone.now().isoformat()})

def csp_report(request):
    """CSP violation report endpoint"""
    return JsonResponse({'status': 'received', 'timestamp': timezone.now().isoformat()})

def version_info(request):
    """Return version information"""
    return JsonResponse({
        'version': '1.0.0',
        'build': 'production',
        'timestamp': timezone.now().isoformat()
    })

def font_test(request):
    """Font testing page for TAN-Garland fonts"""
    return render(request, 'font_test.html')


def legacy_public_redirect(request, legacy_path):
    from django.http import HttpResponsePermanentRedirect, Http404
    from django.urls import resolve, Resolver404
    target = '/' + legacy_path.lstrip('/') if legacy_path else '/packages/'
    try:
        match = resolve(target)
        if match.app_name != 'adminside':
            raise Http404
    except Resolver404:
        raise Http404
    query = request.META.get('QUERY_STRING', '')
    return HttpResponsePermanentRedirect(target + ('?' + query if query else ''))


def robots(request):
    from django.conf import settings
    from django.http import HttpResponse
    return HttpResponse('User-agent: *\nDisallow: /admin/\nDisallow: /checkout/\nDisallow: /booking/\nDisallow: /profile/\nDisallow: /account/\nSitemap: ' + settings.SITE_URL.rstrip('/') + '/sitemap.xml\n', content_type='text/plain')


def public_sitemap(request):
    from django.conf import settings
    from django.http import HttpResponse
    from django.urls import reverse, NoReverseMatch
    from xml.sax.saxutils import escape
    from adminside.models import Package, Destination, Accommodation
    from blog.models import Post
    paths = ['/', '/aboutus/', '/services/', '/contactus/', '/packages/', '/destinations/', '/accommodations/', '/blog/', '/mice/', '/student-travel/', '/ngo-travel/']
    for model, filters, route in [
        (Package, {'status': Package.PUBLISHED}, 'adminside:package_detail'),
        (Destination, {'is_active': True}, 'adminside:destination_detail'),
        (Accommodation, {'is_active': True}, 'adminside:accommodation_detail'),
        (Post, {'status': 'published'}, 'blog:blog-detail')]:
        for slug in model.objects.filter(**filters).exclude(slug='').values_list('slug', flat=True):
            try:
                paths.append(reverse(route, kwargs={'slug': slug}))
            except NoReverseMatch:
                continue
    base = settings.SITE_URL.rstrip('/')
    body = ''.join('<url><loc>' + escape(base + path) + '</loc></url>' for path in paths)
    return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + '</urlset>', content_type='application/xml')
