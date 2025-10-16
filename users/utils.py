from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


class TokenGenerator(PasswordResetTokenGenerator):
	pass

generate_token=TokenGenerator()





def send_booking_confirmation_email(booking):
    """
    Queue booking confirmation email for asynchronous processing
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        from django_q.tasks import async_task

        # Queue the email task for background processing
        task_id = async_task(
            'users.tasks.send_booking_confirmation_email_async',
            booking.id,
            task_name=f'booking_emails_{booking.id}',
            timeout=60,
            retry=5,
        )

        logger.info(f"Booking confirmation email queued: task_id={task_id}, booking_id={booking.id}")
        return True

    except Exception as e:
        logger.error(f"Failed to queue booking confirmation email for {booking.id}: {e}")
        return False