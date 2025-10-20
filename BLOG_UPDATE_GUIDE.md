# Mbugani Luxe Adventures - Blog Update Guide

## Overview

This guide explains how to update the blog content for the Mbugani Luxe Adventures website using the custom Django management command.

## What Was Created

### 1. Management Command
**File:** `blog/management/commands/populate_luxury_blogs.py`

This Django management command:
- Deletes all existing blog posts from the database
- Creates/updates 5 blog categories (Safari Tips, Wildlife & Nature, Destinations, Culture & Heritage, Travel Guides)
- Creates 3 new luxury safari-themed blog posts with full content, tags, and metadata
- All blogs are automatically published and visible on the website

### 2. Helper Script
**File:** `scripts/update_blogs.sh`

A bash script that simplifies running the management command with safety checks for production updates.

### 3. Blog Posts Created

#### Blog Post 1: The Great Migration Guide
- **Title:** "The Great Migration: Your Ultimate Guide to Witnessing Nature's Greatest Spectacle"
- **Category:** Wildlife & Nature
- **Tags:** Great Migration, Maasai Mara, Wildlife Safari, Kenya Safari, Luxury Travel, River Crossing, Wildebeest
- **Status:** Published, Featured, Trending
- **Word Count:** ~1,200 words
- **Content:** Comprehensive guide to experiencing the Great Migration in the Maasai Mara, including timing, accommodations, and photography tips

#### Blog Post 2: Luxury Safari Packing Guide
- **Title:** "The Ultimate Luxury Safari Packing Guide: What to Bring to Kenya"
- **Category:** Safari Tips
- **Tags:** Safari Packing, Travel Tips, Kenya Travel, Safari Guide, Luxury Safari, What to Pack, Safari Essentials
- **Status:** Published, Featured
- **Word Count:** ~1,100 words
- **Content:** Detailed packing guide covering clothing, footwear, photography gear, health essentials, and travel documents

#### Blog Post 3: Amboseli National Park Guide
- **Title:** "Amboseli National Park: Where Elephants Meet Kilimanjaro"
- **Category:** Destinations
- **Tags:** Amboseli, Mount Kilimanjaro, Elephants, Kenya Parks, Wildlife Photography, Luxury Lodges, Safari Destinations
- **Status:** Published, Trending
- **Word Count:** ~1,300 words
- **Content:** In-depth destination guide to Amboseli, featuring elephant viewing, Mount Kilimanjaro, luxury accommodations, and conservation efforts

## How to Use

### Method 1: Using the Helper Script (Recommended)

#### For Development Database:
```bash
./scripts/update_blogs.sh
```

#### For Production Database:
```bash
./scripts/update_blogs.sh --production
```
or
```bash
./scripts/update_blogs.sh -p
```

The production mode includes a confirmation prompt to prevent accidental updates.

### Method 2: Using Django Management Command Directly

#### For Development Database:
```bash
python manage.py populate_luxury_blogs
```

#### For Production Database:
```bash
DJANGO_ENV=production python manage.py populate_luxury_blogs
```

#### Clear Blogs Only (Without Creating New Ones):
```bash
python manage.py populate_luxury_blogs --clear-only
```

## Command Options

### `--clear-only`
Deletes all existing blog posts without creating new ones. Useful for cleaning up the database.

**Example:**
```bash
python manage.py populate_luxury_blogs --clear-only
```

## What Happens When You Run the Command

1. **Step 1: Clear Existing Blogs**
   - All existing blog posts are deleted from the database
   - The count of deleted posts is displayed

2. **Step 2: Create Categories**
   - 5 blog categories are created or updated:
     - Safari Tips
     - Wildlife & Nature
     - Destinations
     - Culture & Heritage
     - Travel Guides

3. **Step 3: Get Admin User**
   - The command finds an admin/staff user to assign as the blog author
   - Prioritizes superusers, then staff users, then any user

4. **Step 4: Create Blog Posts**
   - 3 luxury safari blog posts are created with:
     - Full HTML content (800-1,300 words each)
     - SEO-friendly excerpts
     - Relevant tags
     - Published status
     - Featured/Trending flags
     - Initial view counts

## Verification

After running the command, verify the blogs are visible:

1. **Visit the blog list page:**
   - Development: `http://localhost:8000/blog/`
   - Production: `https://www.mbuganiluxeadventures.com/blog/`

2. **Check individual blog posts:**
   - Click on each blog to ensure content displays correctly
   - Verify images, formatting, and tags

3. **Admin Panel:**
   - Development: `http://localhost:8000/admin/blog/post/`
   - Production: `https://www.mbuganiluxeadventures.com/admin/blog/post/`

## Customizing Blog Content

To modify or add new blog posts, edit the `get_blog_posts_data()` method in:
`blog/management/commands/populate_luxury_blogs.py`

### Blog Post Structure:
```python
{
    'user': author,
    'title': 'Your Blog Title',
    'excerpt': '<p>Brief description for SEO and previews</p>',
    'content': '<h2>Full HTML content...</h2><p>...</p>',
    'category': categories['category-slug'],
    'status': 'published',  # or 'draft', 'in_review'
    'featured': True,  # Show in featured section
    'trending': False,  # Show in trending section
    'views': 0,  # Initial view count
    'tags': ['Tag1', 'Tag2', 'Tag3'],
}
```

## Database Information

### Development Database
- **Type:** SQLite
- **Location:** `mbugani_development.sqlite3`
- **Activated when:** `DJANGO_ENV` is not set or set to 'development'

### Production Database
- **Type:** PostgreSQL (Supabase)
- **Connection:** Configured via `DATABASE_URL` in `.env`
- **Activated when:** `DJANGO_ENV=production`

## Safety Features

1. **Confirmation Prompt:** The helper script requires explicit confirmation before updating production
2. **Clear Logging:** All actions are logged with colored output for easy tracking
3. **Error Handling:** Errors during blog creation are caught and reported without stopping the entire process
4. **Rollback Safe:** Django's transaction management ensures database consistency

## Troubleshooting

### Issue: "No users found in database"
**Solution:** Create at least one user account in the Django admin panel before running the command.

### Issue: Command runs but blogs don't appear on website
**Solution:** 
- Verify blogs are set to `status='published'`
- Clear browser cache
- Check that the blog list view is working correctly

### Issue: Tags not appearing
**Solution:** Ensure `django-taggit` is installed and configured in `INSTALLED_APPS`

### Issue: Images not displaying
**Solution:** 
- The current blog posts use placeholder images from existing assets
- To add custom images, upload them via Uploadcare and update the `image` field in the blog data

## Future Enhancements

To add more blog posts in the future:

1. Open `blog/management/commands/populate_luxury_blogs.py`
2. Add new blog data dictionaries in the `get_blog_posts_data()` method
3. Follow the existing structure for consistency
4. Run the command to update the database

## Support

For issues or questions about the blog update system, refer to:
- Django management commands documentation
- Blog models in `blog/models.py`
- Blog views in `blog/views.py`
- Blog admin configuration in `blog/admin.py`

---

**Last Updated:** 2025-10-20
**Version:** 1.0
**Author:** Mbugani Luxe Adventures Development Team

