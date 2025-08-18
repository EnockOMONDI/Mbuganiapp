# Hero Slider Management System
## Mbugani Luxe Adventures

### Overview
The Hero Slider Management System allows dynamic control of homepage hero images and content through the Django admin panel. This system replaces static hero images with a flexible, database-driven solution.

### Features
- **Dynamic Content**: Manage hero slides through Django admin
- **Image Management**: Upload images using Uploadcare integration
- **Ordering System**: Control slide order with drag-and-drop functionality
- **Active/Inactive Status**: Enable/disable slides without deletion
- **Call-to-Action**: Customizable buttons with URLs
- **Responsive Design**: Optimized for all device sizes
- **Fallback Support**: Default content when no slides are active

### Model Structure

#### HeroSlider Model Fields
```python
- title: CharField (200 chars, optional) - Main headline
- subtitle: CharField (300 chars, optional) - Supporting text
- image: ImageField (Uploadcare) - Hero background image
- is_active: BooleanField - Enable/disable slide
- order: PositiveIntegerField - Display order
- cta_text: CharField (50 chars, optional) - Button text
- cta_url: URLField (optional) - Button destination
- created_at: DateTimeField - Creation timestamp
- updated_at: DateTimeField - Last modification
```

### Admin Panel Usage

#### Accessing Hero Slider Management
1. Login to Django Admin: `/admin/`
2. Navigate to "Adminside" → "Hero Sliders"
3. View all slides in a grid layout with thumbnails

#### Creating New Slides
1. Click "Add Hero Slider"
2. Fill in the form:
   - **Title**: Main headline (optional)
   - **Subtitle**: Supporting text (optional)
   - **Image**: Upload via Uploadcare (recommended: 1920x1080px)
   - **CTA Text**: Button text (e.g., "Book Now")
   - **CTA URL**: Button destination
   - **Active**: Check to enable slide
   - **Order**: Lower numbers appear first

#### Managing Existing Slides
- **Edit**: Click on any slide to modify
- **Quick Toggle**: Use list view to quickly activate/deactivate
- **Reorder**: Change order numbers to rearrange slides
- **Delete**: Remove slides permanently

### Command Line Management

#### Available Commands
```bash
# List all hero sliders
python manage.py manage_hero_slider --list

# Create new slider
python manage.py manage_hero_slider --create --title "Your Title" --subtitle "Your Subtitle" --order 1

# Activate slider
python manage.py manage_hero_slider --activate 1

# Deactivate slider
python manage.py manage_hero_slider --deactivate 1

# Delete slider
python manage.py manage_hero_slider --delete 1
```

### Template Integration

#### How It Works
The homepage template (`indexbackup.html`) automatically loads active hero slides:

```django
{% if hero_slides %}
    {% for slide in hero_slides %}
        <!-- Dynamic slide content -->
    {% endfor %}
{% else %}
    <!-- Fallback default slide -->
{% endif %}
```

#### Fallback Behavior
- If no active slides exist, displays default content
- Uses static image: `assets/images/hero/2.png`
- Shows default Mbugani Luxe Adventures messaging

### Best Practices

#### Image Guidelines
- **Recommended Size**: 1920x1080px (16:9 aspect ratio)
- **File Format**: JPG or PNG
- **File Size**: Under 2MB for optimal loading
- **Content**: Ensure text overlay areas are not too busy

#### Content Guidelines
- **Title**: Keep under 60 characters for mobile compatibility
- **Subtitle**: Maximum 150 characters for readability
- **CTA Text**: Use action words (Book, Explore, Discover)
- **CTA URL**: Use relative URLs when possible

#### Performance Tips
- Limit active slides to 3-5 for optimal performance
- Use Uploadcare's CDN features for image optimization
- Test on mobile devices for text readability

### Troubleshooting

#### Common Issues
1. **Slides not appearing**: Check if slides are marked as active
2. **Images not loading**: Verify Uploadcare configuration
3. **Order not working**: Ensure order numbers are different
4. **Mobile display issues**: Check image aspect ratios

#### Debug Commands
```bash
# Check slide status
python manage.py manage_hero_slider --list

# Verify database
python manage.py shell
>>> from adminside.models import HeroSlider
>>> HeroSlider.objects.all()
```

### Technical Details

#### Database Migration
- Migration file: `0006_add_hero_slider.py`
- Data migration: `0007_populate_default_hero_slider.py`

#### Dependencies
- Django ImageField (Uploadcare)
- Custom admin CSS: `unfold-custom.css`
- Management command: `manage_hero_slider.py`

#### Security Considerations
- Admin access required for modifications
- Image uploads validated through Uploadcare
- URL validation for CTA links
- XSS protection in template rendering

### Future Enhancements
- Video background support
- Animation effects configuration
- A/B testing capabilities
- Analytics integration
- Scheduled slide activation
