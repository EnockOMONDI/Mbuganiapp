#!/usr/bin/env python
"""
Test Gmail SMTP connection directly
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_connection():
    """Test direct connection to Gmail SMTP"""
    
    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "mbuganiluxeadventures@gmail.com"
    password = "grdg fofh myne wdpf"
    
    print("🧪 Testing direct Gmail SMTP connection...")
    print(f"📧 Email: {sender_email}")
    print(f"🌐 Server: {smtp_server}:{port}")
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Enable security
        server.login(sender_email, password)
        
        print("✅ Gmail SMTP connection successful!")
        print("✅ Authentication successful!")
        
        # Send a test email
        receiver_email = "djsean@mbuganiluxeadventures.com"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Email - Mbugani Luxe Adventures"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        # Create the HTML content
        html = """
        <html>
          <body>
            <h2>Test Email from Mbugani Luxe Adventures</h2>
            <p>This is a test email to verify Gmail SMTP configuration.</p>
            <p>If you receive this email, the configuration is working correctly!</p>
          </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print(f"✅ Test email sent successfully to {receiver_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("🔍 Check if:")
        print("   - Gmail account has 2FA enabled")
        print("   - App password is correct and not expired")
        print("   - Account is not suspended")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("🔍 Check if:")
        print("   - Internet connection is working")
        print("   - Firewall is not blocking port 587")
        print("   - SMTP server address is correct")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    if success:
        print("\n🎉 Gmail SMTP configuration is working correctly!")
    else:
        print("\n❌ Gmail SMTP configuration needs to be fixed.")
