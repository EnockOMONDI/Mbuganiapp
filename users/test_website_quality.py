from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase, override_settings, Client
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils import timezone
from adminside.models import Package, Destination
from adminside.templatetags.image_tags import image_with_placeholder
from users.models import Booking, BookingAccessChallenge, EmailDelivery, QuoteRequest
from users.forms import QuoteRequestForm
from users.checkout_views import create_booking_from_cart, send_welcome_email
from users.tasks import send_email_via_mailtrap, deliver_email

@override_settings(SECURE_SSL_REDIRECT=False, ALLOWED_HOSTS=['testserver'], SITE_URL='http://testserver',
                   DEFAULT_FROM_EMAIL='info@example.com', ADMIN_EMAIL='admin@example.com', MAILTRAP_API_TOKEN='test')
class WebsiteQualityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.destination=Destination.objects.create(name='Kenya',slug='kenya',destination_type='country')
        cls.package=Package.objects.create(name='Safari',slug='safari',main_destination=cls.destination,
            duration_days=3,duration_nights=2,adult_price=100,child_price=50,status='published')
        cls.user=User.objects.create_user('owner',email='owner@example.com',password='secret-test')
        cls.booking=Booking.objects.create(package=cls.package,user=cls.user,full_name='Private Guest',
            email='owner@example.com',phone_number='+254000000000',package_price=100,total_amount=100)

    def test_confirmation_never_discloses_details_until_verified(self):
        url=reverse('users:booking_confirmation',args=[self.booking.booking_reference])
        self.assertNotContains(self.client.get(url),'Private Guest')
        with patch('users.tasks.send_email_via_mailtrap',return_value=True) as send, patch('users.booking_access.secrets.randbelow',return_value=123456):
            self.client.post(url,{'email':'wrong@example.com'})
            send.assert_not_called()
            # Different reference has an independent rate bucket.
            BookingAccessChallenge.objects.all().delete()
            self.client.post(url,{'email':self.booking.email})
            self.assertEqual(send.call_count,1)
            denied=self.client.post(url,{'email':self.booking.email,'code':'000000'})
            self.assertNotContains(denied,'Private Guest')
            granted=self.client.post(url,{'email':self.booking.email,'code':'123456'})
            self.assertEqual(granted.status_code,302)
            self.assertContains(self.client.get(url),'Private Guest')
            self.assertIn('no-store', self.client.get(url)['Cache-Control'])
        other=Client()
        self.assertNotContains(other.get(url),'Private Guest')

    def test_confirmation_expiry_and_rate_limit_survive_new_sessions(self):
        url=reverse('users:booking_confirmation',args=[self.booking.booking_reference])
        with patch('users.tasks.send_email_via_mailtrap',return_value=True) as send, patch('users.booking_access.secrets.randbelow',return_value=123456):
            self.client.post(url,{'email':self.booking.email})
            Client().post(url,{'email':self.booking.email})
            self.assertEqual(send.call_count,1)
            BookingAccessChallenge.objects.update(expires_at=timezone.now()-timedelta(seconds=1))
            response=self.client.post(url,{'email':self.booking.email,'code':'123456'})
            self.assertNotContains(response,'Private Guest')

    def test_owner_access_and_other_user_denied(self):
        url=reverse('users:booking_confirmation',args=[self.booking.booking_reference])
        self.client.force_login(self.user)
        self.assertContains(self.client.get(url),'Private Guest')
        stranger=User.objects.create_user('stranger',email='stranger@example.com')
        self.client.force_login(stranger)
        self.assertNotContains(self.client.get(url),'Private Guest')

    def test_guest_cannot_attach_existing_account(self):
        from types import SimpleNamespace
        cart=SimpleNamespace(get_cart_items=lambda:[{'package':self.package,'adults':1,'children':0,'rooms':1,'accommodations':[],'travel_modes':[]}])
        data={'full_name':'Test Guest','email':self.user.email,'phone_number':'+254000000000'}
        booking=create_booking_from_cart(cart,data)
        self.assertIsNone(booking.user_id)
        with patch('users.checkout_views.send_welcome_email') as send:
            data['email']='new@example.com'
            booking=create_booking_from_cart(cart,data)
            self.assertFalse(booking.user.has_usable_password())
            send.assert_called_once_with(booking.user)

    def test_invitation_has_no_password_and_token_invalidates(self):
        with patch('users.tasks.send_email_via_mailtrap',return_value=True) as send:
            send_welcome_email(self.user)
            html=send.call_args.kwargs['html_message']
            self.assertIn('/account/set-password/',html)
            self.assertNotIn('Temporary Password',html)
        token=default_token_generator.make_token(self.user)
        self.user.set_password('replacement-test');self.user.save()
        self.assertFalse(default_token_generator.check_token(self.user,token))

    def test_legacy_redirect_preserves_query_and_clean_links(self):
        response=self.client.get('/adminside/packages/?page=2&search=lake%20view')
        self.assertEqual(response.status_code,301)
        self.assertEqual(response.url,'/packages/?page=2&search=lake%20view')
        self.assertEqual(self.package.get_absolute_url(),'/packages/safari/')
        for path in ['/sitemap.xml','/robots.txt','/quote/?package_id=oops','/packages/?destination=oops','/contactus/']:
            self.assertEqual(self.client.get(path).status_code,200,path)

    def test_pagination_second_page_and_filter_encoding(self):
        for n in range(14):
            Package.objects.create(name=f'Safari {n}',slug=f'safari-{n}',main_destination=self.destination,
                duration_days=1,duration_nights=0,adult_price=1,child_price=0,status='published')
        response=self.client.get('/packages/?page=2&destination='+str(self.destination.pk))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['page_obj']),3)
        self.assertContains(response,'destination='+str(self.destination.pk))
        self.assertContains(response,'Previous')
        self.assertEqual(self.client.get('/packages/?page=bogus').status_code,200)
        self.assertEqual(self.client.get('/packages/?page=9999').status_code,200)

    def test_image_attributes_are_escaped_and_stale_image_falls_back(self):
        class BrokenImage:
            @property
            def url(self): raise ValueError('No file')
        html=str(image_with_placeholder(BrokenImage(),alt_text='" onerror="alert(1)'))
        self.assertIn('placeholder.svg',html)
        self.assertIn('&quot;',html)
        self.assertNotIn('alt="" onerror=',html)

    def test_quote_dates_and_contact_persistence_on_delivery_failure(self):
        data={'full_name':'Test Guest','email':'qa@example.com','phone_number':'+254000000000',
              'destination':'Kenya','number_of_travelers':2,'start_date':'2020-01-01'}
        self.assertFalse(QuoteRequestForm(data).is_valid())
        data.update(start_date='',flexible_dates='on')
        form=QuoteRequestForm(data);self.assertTrue(form.is_valid(),form.errors)
        self.assertEqual(form.save().preferred_travel_dates,'Flexible dates')
        with patch('users.tasks.send_quote_request_emails',return_value={'success':False}):
            response=self.client.post('/contactus/',{'full_name':'Test Guest','email':'qa@example.com','special_requests':'TEST ONLY'})
        self.assertEqual(response.status_code,302)
        self.assertTrue(QuoteRequest.objects.filter(destination='General enquiry').exists())

    def test_email_failure_is_durable_then_retried_without_resending_success(self):
        with patch('users.tasks._send_email_via_mailtrap',return_value=False):
            self.assertFalse(send_email_via_mailtrap('Test','body','info@example.com',['qa@example.com']))
        delivery=EmailDelivery.objects.get();self.assertEqual(delivery.attempts,1)
        EmailDelivery.objects.update(next_attempt_at=timezone.now()-timedelta(seconds=1))
        with patch('users.tasks._send_email_via_mailtrap',return_value=True) as send:
            self.assertTrue(deliver_email(delivery.pk));self.assertTrue(deliver_email(delivery.pk))
            self.assertEqual(send.call_count,1)
        delivery.refresh_from_db();self.assertIsNotNone(delivery.sent_at);self.assertEqual(delivery.html_message,'')

    def test_cart_remove_requires_post_and_bad_counts_do_not_crash(self):
        self.assertEqual(self.client.get(reverse('users:remove_from_cart',args=[self.package.pk])).status_code,405)
        response=self.client.post(reverse('users:add_to_cart',args=[self.package.pk]),{'adults':'bad','children':-1,'rooms':0})
        self.assertEqual(response.status_code,302)

    def test_legacy_blank_slugs_render_instead_of_crashing_lists(self):
        from blog.models import Post
        Package.objects.filter(pk=self.package.pk).update(slug='')
        self.assertEqual(self.client.get('/packages/').status_code,200)
        self.package.refresh_from_db()
        self.assertEqual(self.client.get(self.package.get_absolute_url()).status_code,200)
        post=Post.objects.create(title='Travel story',content='A story',status='published')
        Post.objects.filter(pk=post.pk).update(slug='')
        self.assertEqual(self.client.get('/blog/').status_code,200)
        post.refresh_from_db()
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code,200)

    def test_expired_email_is_not_retried(self):
        email=EmailDelivery.objects.create(subject='Code',html_message='123456',from_email='info@example.com',
            recipients=['qa@example.com'],expires_at=timezone.now()-timedelta(seconds=1))
        with patch('users.tasks._send_email_via_mailtrap') as send:
            self.assertFalse(deliver_email(email.pk));send.assert_not_called()
        email.refresh_from_db();self.assertEqual(email.html_message,'')

    def test_unusable_password_invitation_can_be_completed_once(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        invited=User.objects.create_user('invited@example.com',email='invited@example.com',password=None)
        url=reverse('users:set_password',kwargs={'uidb64':urlsafe_base64_encode(force_bytes(invited.pk)),
            'token':default_token_generator.make_token(invited)})
        response=self.client.get(url)
        self.assertEqual(response.status_code,302)
        response=self.client.post(response.url,{'new_password1':'SecureExampleOnly892!', 'new_password2':'SecureExampleOnly892!'})
        self.assertEqual(response.status_code,302)
        invited.refresh_from_db();self.assertTrue(invited.has_usable_password())
        self.assertContains(Client().get(url),'expired')

    def test_destination_search_finds_nested_places_and_filters_countries(self):
        city=Destination.objects.create(name='Nairobi',slug='nairobi',destination_type='city',parent=self.destination)
        Destination.objects.create(name='National Park',slug='national-park',destination_type='place',parent=city)
        response=self.client.get('/destinations/?search=National+Park')
        self.assertEqual(response.status_code,200)
        self.assertEqual(list(response.context['countries']),[self.destination])
        self.assertContains(response,'National Park')
        response=self.client.get('/destinations/?country=missing')
        self.assertContains(response,'No destinations found')
