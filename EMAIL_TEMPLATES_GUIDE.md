# Mbugani Luxe Adventures - Email Templates Guide

## Overview
All email templates have been updated with the complete Mbugani Luxe Adventures branding, featuring luxury safari tourism aesthetic and consistent messaging.

## Brand Elements Applied

### Visual Identity
- **Company Name**: Mbugani Luxe Adventures
- **Tagline**: "Untamed. Unmatched. Unforgettable."
- **Color Scheme**: 
  - Primary: #291c1b (Burgundy)
  - Secondary: #fb9300 (Orange)
  - Gradient: `linear-gradient(135deg, #291c1b, #fb9300)`
- **Typography**: 'TAN-Garland-Regular' with fallbacks to Georgia, Times New Roman, serif

### Contact Information
- **Email**: info@mbuganiluxeadventures.com
- **Phone**: +254 798 197 430
- **Location**: Nairobi, Kenya
- **Website**: www.mbuganiluxeadventures.com

## Email Templates Inventory

### 1. Customer-Facing Templates

#### Booking Confirmation (`users/emails/booking_confirmation.html`)
- **Purpose**: Sent when customers complete a booking
- **Features**: 
  - Booking reference number
  - Package details and pricing
  - Customer information summary
  - Next steps and contact information
  - Dashboard access link

#### Welcome Email (`users/emails/welcome.html`)
- **Purpose**: Sent to new users after account creation
- **Features**:
  - Account credentials for new users
  - Platform introduction
  - Dashboard access instructions
  - Travel community welcome message

#### Newsletter Confirmation (`users/emails/newsletter_confirmation.html`)
- **Purpose**: Confirms newsletter subscription
- **Features**:
  - Subscription preferences summary
  - What to expect from newsletter
  - Contact information
  - Unsubscribe options

#### Job Application Confirmation (`users/emails/job_application_confirmation.html`)
- **Purpose**: Confirms receipt of job applications
- **Features**:
  - Application details summary
  - Next steps in hiring process
  - HR contact information
  - Professional branding

#### Password Reset (`templates/registration/password_reset_email.html`)
- **Purpose**: Django password reset functionality
- **Features**:
  - Secure reset link
  - Security notices
  - 24-hour expiration notice
  - Support contact information

### 2. Administrative Templates

#### Admin Notification (`users/emails/admin_notification.html`)
- **Purpose**: Alerts admin team of new bookings
- **Features**:
  - Immediate attention alerts
  - Complete booking details
  - Customer contact information
  - Action items checklist
  - Revenue breakdown

#### Newsletter Admin (`users/emails/newsletter_admin.html`)
- **Purpose**: Notifies admin of new newsletter subscriptions
- **Features**:
  - Subscriber details
  - Subscription preferences
  - Admin action items
  - Growth tracking information

#### Job Application Admin (`users/emails/job_application_admin.html`)
- **Purpose**: Notifies HR of new job applications
- **Features**:
  - Application summary
  - Candidate qualifications
  - Review requirements
  - HR workflow integration

### 3. Base Template

#### Base Email Template (`users/emails/base_email.html`)
- **Purpose**: Reusable template for future emails
- **Features**:
  - Consistent Mbugani branding
  - Responsive design
  - Block structure for customization
  - Email client compatibility
  - Luxury styling elements

## Design Standards

### Layout Structure
1. **Header**: Gradient background with company name and tagline
2. **Content**: White background with luxury accent elements
3. **Footer**: Light background with contact info and social links

### Typography Hierarchy
- **H1**: 28px, TAN-Garland-Regular, white (headers)
- **H2**: 24px, TAN-Garland-Regular, #291c1b (content headings)
- **H3**: 18px, regular weight, #291c1b (subheadings)
- **Body**: 16px, Arial/Helvetica, #333 (main content)

### Interactive Elements
- **Primary Buttons**: Burgundy gradient, white text, rounded corners
- **Secondary Buttons**: Orange gradient, burgundy text, rounded corners
- **Links**: Burgundy color with hover effects

### Responsive Design
- **Mobile Breakpoint**: 600px
- **Adjustments**: Reduced padding, stacked buttons, smaller fonts
- **Email Client Compatibility**: Fallback fonts and table-based layouts

## Email Configuration

### SMTP Settings
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mbuganiluxeadventures@gmail.com'  # Maintained for continuity
DEFAULT_FROM_EMAIL = 'Mbugani Luxe Adventures <mbuganiluxeadventures@gmail.com>'
```

### Email Addresses
- **General**: info@mbuganiluxeadventures.com
- **Careers**: careers@mbuganiluxeadventures.com
- **Newsletter**: news@mbuganiluxeadventures.com
- **Admin**: admin@mbuganiluxeadventures.com

## Testing and Quality Assurance

### Template Testing
Use the management command to test all templates:
```bash
python manage.py test_email_templates
```

### Checklist for New Templates
- [ ] Mbugani Luxe Adventures branding applied
- [ ] Correct phone number (+254 798 197 430)
- [ ] Proper email addresses used
- [ ] Responsive design implemented
- [ ] Brand colors (#291c1b, #fb9300) included
- [ ] Fallback fonts specified
- [ ] Contact information in footer
- [ ] Unsubscribe/disclaimer text included

## Best Practices

### Content Guidelines
1. **Tone**: Professional yet warm, reflecting luxury positioning
2. **Language**: Clear, concise, and action-oriented
3. **Personalization**: Use customer names and relevant details
4. **Call-to-Action**: Clear next steps for recipients

### Technical Guidelines
1. **File Size**: Keep images optimized and emails under 100KB
2. **Testing**: Test across multiple email clients
3. **Accessibility**: Include alt text and proper contrast ratios
4. **Security**: Use HTTPS links and secure practices

### Maintenance
1. **Regular Updates**: Review templates quarterly
2. **Performance Monitoring**: Track open and click rates
3. **Brand Consistency**: Ensure alignment with website updates
4. **Legal Compliance**: Include required unsubscribe and privacy information

## Future Enhancements

### Planned Improvements
1. **Email Analytics**: Integration with tracking systems
2. **A/B Testing**: Template variation testing
3. **Personalization**: Dynamic content based on user preferences
4. **Automation**: Triggered email sequences
5. **Multi-language**: Support for multiple languages

This guide ensures all email communications maintain the sophisticated Mbugani Luxe Adventures brand identity while providing excellent customer experience.
