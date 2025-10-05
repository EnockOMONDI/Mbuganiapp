"""
Custom SMTP Email Backend for Mbugani Luxe Adventures
Handles SSL certificate issues in local development environments
"""
import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend


class CustomSMTPBackend(EmailBackend):
    """
    Custom SMTP backend that handles SSL certificate verification issues
    in local development environments while maintaining security in production.
    """

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 ssl_keyfile=None, ssl_certfile=None):
        super().__init__(host, port, username, password, use_tls, fail_silently,
                        use_ssl, timeout, ssl_keyfile, ssl_certfile)
        self._connection_opened = False

    def open(self):
        """
        Open a connection to the SMTP server with custom SSL handling.
        Optimized for production environments with proper timeout handling.
        """
        if self.connection:
            return False

        # Use shorter timeout for production to prevent worker timeouts
        connection_timeout = min(self.timeout or 30, 10)  # Max 10 seconds for production

        try:
            # Create SMTP connection with shorter timeout
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(self.host, self.port, timeout=connection_timeout)
            else:
                self.connection = smtplib.SMTP(self.host, self.port, timeout=connection_timeout)

            # Set debug level if needed
            if hasattr(self, '_debug') and self._debug:
                self.connection.set_debuglevel(1)

            # Handle TLS/SSL upgrade
            if not self.use_ssl and self.use_tls:
                # Create SSL context with proper timeout
                context = ssl.create_default_context()
                context.check_hostname = True
                context.verify_mode = ssl.CERT_REQUIRED

                # Set SSL socket timeout
                self.connection.sock.settimeout(connection_timeout)

                try:
                    self.connection.starttls(context=context)
                except ssl.SSLError as e:
                    # In production, we should NOT disable SSL verification
                    # Instead, let the error propagate so it can be handled properly
                    raise e

                # Re-issue EHLO after STARTTLS
                try:
                    self.connection.ehlo()
                except Exception as ehlo_error:
                    try:
                        self.connection.close()
                    except:
                        pass
                    raise ehlo_error

            # Authenticate if credentials provided
            if self.username and self.password:
                try:
                    self.connection.login(self.username, self.password)
                except Exception as auth_error:
                    try:
                        self.connection.close()
                    except:
                        pass
                    raise auth_error

            return True

        except Exception as e:
            # Ensure connection is cleaned up on any error
            if hasattr(self, 'connection') and self.connection:
                try:
                    self.connection.close()
                except:
                    pass
                self.connection = None

            if not self.fail_silently:
                raise
            return False

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent. Optimized for production with robust error handling.
        """
        if not email_messages:
            return 0

        num_sent = 0
        # Use context manager with comprehensive error handling
        try:
            with self:
                for message in email_messages:
                    try:
                        sent = self._send(message)
                        if sent:
                            num_sent += 1
                    except Exception as e:
                        # Log individual message errors but continue processing others
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Failed to send email to {getattr(message, 'to', 'unknown')}: {e}")
                        # Continue with other messages - don't fail the entire batch

        except Exception as e:
            # If the context manager fails, log the error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Email backend context manager failed: {e}")
            # Don't re-raise to prevent worker crashes

        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not self.connection:
            # We failed silently on open(), trying again will not help.
            return False

        try:
            # Quick connection check
            if hasattr(self.connection, 'noop'):
                try:
                    self.connection.noop()
                except:
                    # Connection is dead, try to reopen
                    self.close()
                    if not self.open():
                        return False

            # Send the message
            result = super()._send(email_message)
            return result

        except Exception as e:
            # If sending fails, close the connection so it gets reopened on next attempt
            try:
                self.close()
            except:
                pass

            if not self.fail_silently:
                raise
            return False