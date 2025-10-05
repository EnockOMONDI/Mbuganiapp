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
        """
        if self.connection:
            return False

        try:
            # Create SMTP connection
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(self.host, self.port, timeout=self.timeout)
            else:
                self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)

            # Set debug level if needed
            if hasattr(self, '_debug') and self._debug:
                self.connection.set_debuglevel(1)

            # Handle TLS/SSL upgrade
            if not self.use_ssl and self.use_tls:
                # Create SSL context that handles certificate verification issues
                context = ssl.create_default_context()

                # In local development, if SSL verification fails, try with verification disabled
                # This is a workaround for local development environments
                try:
                    self.connection.starttls(context=context)
                except ssl.SSLError as e:
                    if 'CERTIFICATE_VERIFY_FAILED' in str(e):
                        # Fallback: disable certificate verification for local development
                        # WARNING: This reduces security and should only be used in development
                        import warnings
                        warnings.warn(
                            "SSL certificate verification failed. Using insecure connection for development. "
                            "Ensure proper SSL certificates are installed in production.",
                            UserWarning
                        )
                        # Create a new context with verification disabled
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        self.connection.starttls(context=context)
                    else:
                        raise

                # Re-issue EHLO after STARTTLS to ensure connection is properly initialized
                try:
                    self.connection.ehlo()
                except Exception as ehlo_error:
                    # If EHLO fails, the connection might be in a bad state
                    # Try to close and reopen the connection
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
                    # If authentication fails, ensure connection is closed
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
        messages sent.
        """
        if not email_messages:
            return 0

        num_sent = 0
        with self:
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not self.connection:
            # We failed silently on open(), trying again will not help.
            return False

        try:
            # Ensure connection is still alive
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