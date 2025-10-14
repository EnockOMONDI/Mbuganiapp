#!/usr/bin/env python3
"""
Gmail Credentials Tester for Mbugani Luxe Adventures
====================================================

This script tests Gmail SMTP credentials to verify they work before deploying.

Usage:
    # Test Novustell production password
    python test_gmail_credentials.py --novustell-prod
    
    # Test Novustell development password
    python test_gmail_credentials.py --novustell-dev
    
    # Test Mbugani Gmail account
    python test_gmail_credentials.py --mbugani
    
    # Test custom credentials
    python test_gmail_credentials.py --custom user@gmail.com "app password"

Author: Mbugani Luxe Adventures Development Team
Date: October 7, 2025
"""

import smtplib
import sys
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Predefined credentials
CREDENTIALS = {
    'novustell_dev': {
        'email': 'novustellke@gmail.com',
        'password': 'vsmw vdut tanu gtdg',
        'name': 'Novustell Development'
    },
    'novustell_prod': {
        'email': 'novustellke@gmail.com',
        'password': 'iagt yans hoyd pavg',
        'name': 'Novustell Production'
    },
    'mbugani': {
        'email': 'mbuganiluxeadventures@gmail.com',
        'password': 'grdg fofh myne wdpf',
        'name': 'Mbugani Luxe Adventures'
    }
}

def print_header():
    """Print test header"""
    print("=" * 80)
    print(f"{BLUE}🔐 Gmail SMTP Credentials Tester{RESET}")
    print("=" * 80)
    print()

def print_test_info(credential_name, email, password_masked):
    """Print test information"""
    print(f"{YELLOW}Testing Credentials:{RESET}")
    print(f"  Account: {credential_name}")
    print(f"  Email: {email}")
    print(f"  Password: {password_masked}")
    print(f"  SMTP Server: smtp.gmail.com:587")
    print(f"  TLS: Enabled")
    print()

def mask_password(password):
    """Mask password for display"""
    if len(password) <= 4:
        return "****"
    return password[:4] + "*" * (len(password) - 4)

def test_smtp_connection(email, password, credential_name):
    """Test SMTP connection and authentication"""
    print(f"{BLUE}Step 1: Testing SMTP Connection...{RESET}")
    
    try:
        # Create SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        print(f"{GREEN}✅ Connected to smtp.gmail.com:587{RESET}")
        
        # Start TLS
        print(f"{BLUE}Step 2: Starting TLS encryption...{RESET}")
        server.starttls()
        print(f"{GREEN}✅ TLS encryption enabled{RESET}")
        
        # Authenticate
        print(f"{BLUE}Step 3: Authenticating with Gmail...{RESET}")
        server.login(email, password)
        print(f"{GREEN}✅ Authentication successful!{RESET}")
        
        # Close connection
        server.quit()
        print(f"{GREEN}✅ Connection closed cleanly{RESET}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"{RED}❌ Authentication failed!{RESET}")
        print(f"{RED}Error: {str(e)}{RESET}")
        print()
        print(f"{YELLOW}Possible causes:{RESET}")
        print("  1. Incorrect password")
        print("  2. 2-Factor Authentication not enabled")
        print("  3. App password not created")
        print("  4. Account security settings blocking access")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"{RED}❌ Connection failed!{RESET}")
        print(f"{RED}Error: {str(e)}{RESET}")
        print()
        print(f"{YELLOW}Possible causes:{RESET}")
        print("  1. No internet connection")
        print("  2. Firewall blocking port 587")
        print("  3. Gmail SMTP server down (unlikely)")
        return False
        
    except Exception as e:
        print(f"{RED}❌ Unexpected error!{RESET}")
        print(f"{RED}Error: {str(e)}{RESET}")
        return False

def test_email_sending(email, password, credential_name, test_recipient=None):
    """Test actual email sending"""
    if not test_recipient:
        print()
        print(f"{YELLOW}Skipping email send test (no recipient specified){RESET}")
        return True
    
    print()
    print(f"{BLUE}Step 4: Testing Email Sending...{RESET}")
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Test Email from {credential_name}'
        msg['From'] = f'{credential_name} <{email}>'
        msg['To'] = test_recipient
        
        # Email body
        text = f"""
        This is a test email from the Mbugani Luxe Adventures email system.
        
        Credentials tested: {credential_name}
        Sent from: {email}
        Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
        
        If you received this email, the SMTP configuration is working correctly!
        """
        
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #291c1a;">✅ Email System Test Successful</h2>
            <p>This is a test email from the <strong>Mbugani Luxe Adventures</strong> email system.</p>
            <hr>
            <p><strong>Test Details:</strong></p>
            <ul>
              <li>Credentials: {credential_name}</li>
              <li>Sent from: {email}</li>
              <li>Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <hr>
            <p style="color: #28a745;">If you received this email, the SMTP configuration is working correctly!</p>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        
        print(f"{GREEN}✅ Test email sent successfully to {test_recipient}!{RESET}")
        print(f"{YELLOW}Check your inbox (may take 1-2 minutes){RESET}")
        
        return True
        
    except Exception as e:
        print(f"{RED}❌ Email sending failed!{RESET}")
        print(f"{RED}Error: {str(e)}{RESET}")
        return False

def print_summary(success, credential_name):
    """Print test summary"""
    print()
    print("=" * 80)
    if success:
        print(f"{GREEN}🎉 SUCCESS! {credential_name} credentials are working!{RESET}")
        print()
        print(f"{YELLOW}Next Steps:{RESET}")
        print("  1. Update Render environment variables with these credentials")
        print("  2. Deploy to production")
        print("  3. Test quote request on live site")
    else:
        print(f"{RED}❌ FAILED! {credential_name} credentials are NOT working!{RESET}")
        print()
        print(f"{YELLOW}Troubleshooting:{RESET}")
        print("  1. Verify the password is correct")
        print("  2. Check if 2FA is enabled on the Gmail account")
        print("  3. Create a new app password if needed")
        print("  4. Try a different set of credentials")
    print("=" * 80)

def main():
    """Main test function"""
    parser = argparse.ArgumentParser(description='Test Gmail SMTP credentials')
    parser.add_argument('--novustell-dev', action='store_true', 
                       help='Test Novustell development credentials')
    parser.add_argument('--novustell-prod', action='store_true', 
                       help='Test Novustell production credentials')
    parser.add_argument('--mbugani', action='store_true', 
                       help='Test Mbugani Gmail credentials')
    parser.add_argument('--custom', nargs=2, metavar=('EMAIL', 'PASSWORD'),
                       help='Test custom credentials')
    parser.add_argument('--send-test', metavar='RECIPIENT_EMAIL',
                       help='Send a test email to this address')
    
    args = parser.parse_args()
    
    print_header()
    
    # Determine which credentials to test
    if args.novustell_dev:
        creds = CREDENTIALS['novustell_dev']
        email = creds['email']
        password = creds['password']
        name = creds['name']
    elif args.novustell_prod:
        creds = CREDENTIALS['novustell_prod']
        email = creds['email']
        password = creds['password']
        name = creds['name']
    elif args.mbugani:
        creds = CREDENTIALS['mbugani']
        email = creds['email']
        password = creds['password']
        name = creds['name']
    elif args.custom:
        email = args.custom[0]
        password = args.custom[1]
        name = f"Custom ({email})"
    else:
        print(f"{RED}Error: Please specify which credentials to test{RESET}")
        print()
        print("Examples:")
        print("  python test_gmail_credentials.py --novustell-prod")
        print("  python test_gmail_credentials.py --mbugani")
        print("  python test_gmail_credentials.py --custom user@gmail.com 'app password'")
        sys.exit(1)
    
    # Print test info
    print_test_info(name, email, mask_password(password))
    
    # Test SMTP connection
    success = test_smtp_connection(email, password, name)
    
    # Test email sending if requested and connection succeeded
    if success and args.send_test:
        success = test_email_sending(email, password, name, args.send_test)
    
    # Print summary
    print_summary(success, name)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

