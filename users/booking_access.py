"""Email possession check before a guest can view a booking."""
import hashlib
import secrets
from datetime import timedelta
from django import forms
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.html import format_html
from django.views.decorators.cache import never_cache
from .models import Booking, BookingAccessChallenge


class AccessForm(forms.Form):
    email = forms.EmailField(label='Booking email', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    code = forms.CharField(required=False, max_length=6, label='Email verification code',
                           widget=forms.TextInput(attrs={'inputmode': 'numeric', 'autocomplete': 'one-time-code'}))


def confirmation_access(request, reference):
    booking = Booking.objects.select_related('package').filter(booking_reference=reference).first()
    if booking and request.user.is_authenticated and booking.user_id == request.user.pk:
        return booking, None
    grants = request.session.get('booking_access', {})
    if booking and grants.get(reference, 0) > timezone.now().timestamp():
        return booking, None
    form = AccessForm(request.POST or None)
    notice = ''
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].casefold()
        if not request.session.session_key:
            request.session.create()
        # A persistent bucket limits both code sends and guesses, including unknown references.
        key = hashlib.sha256(reference.encode()).hexdigest()
        now = timezone.now()
        send_code = None
        with transaction.atomic():
            challenge, _ = BookingAccessChallenge.objects.select_for_update().get_or_create(key=key)
            if challenge.window_started < now - timedelta(hours=1):
                challenge.attempts = 0
                challenge.sends = 0
                challenge.window_started = now
            challenge.attempts += 1
            code = form.cleaned_data.get('code')
            if code:
                digest = salted_hmac('booking-code', code).hexdigest()
                valid = (challenge.attempts <= 12 and challenge.expires_at and challenge.expires_at > now
                         and secrets.compare_digest(challenge.code_hash, digest)
                         and booking and secrets.compare_digest(booking.email.casefold(), email))
                if valid:
                    challenge.code_hash = ''
                    challenge.save()
                    grants[reference] = (now + timedelta(minutes=30)).timestamp()
                    request.session['booking_access'] = grants
                    return None, redirect('users:booking_confirmation', booking_reference=reference)
                notice = 'The code is invalid or expired. Request a new code if needed.'
            else:
                notice = 'If the details match a booking, a verification code will be emailed. It expires in 10 minutes.'
                if challenge.sends < 3 and challenge.attempts <= 12 and (not challenge.last_sent or challenge.last_sent < now - timedelta(seconds=60)):
                    challenge.sends += 1
                    challenge.last_sent = now
                    if booking and secrets.compare_digest(booking.email.casefold(), email):
                        send_code = str(secrets.randbelow(1000000)).zfill(6)
                        challenge.code_hash = salted_hmac('booking-code', send_code).hexdigest()
                        challenge.expires_at = now + timedelta(minutes=10)
            challenge.save()
        if send_code:
            from .tasks import send_email_via_mailtrap
            send_email_via_mailtrap('Your Mbugani booking verification code',
                format_html('<p>Your verification code is <strong>{}</strong>.</p><p>It expires in 10 minutes. If you did not request it, ignore this email.</p>', send_code),
                settings.DEFAULT_FROM_EMAIL, [booking.email], expires_at=now + timedelta(minutes=10))
    response = render(request, 'users/booking_access.html', {'form': form, 'notice': notice, 'page_title': 'View your booking'})
    response['Cache-Control'] = 'no-store, private'
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return None, response
