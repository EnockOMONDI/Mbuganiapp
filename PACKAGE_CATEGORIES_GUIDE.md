# Package Categories System - Mbugani Luxe Adventures

## Overview

This guide explains the new package categorization system for Mbugani Luxe Adventures. The system organizes travel packages into three main categories to improve navigation and user experience.

---

## Package Categories

### 1. **Nairobi Excursions**
- **Slug**: `nairobi-excursions`
- **Description**: One-day packages and tours within Nairobi and surrounding areas
- **Purpose**: For day trips, city tours, and short excursions that don't require overnight stays
- **Examples**:
  - Nairobi National Park Excursion Tour
  - Nairobi Heritage Excursion Tour
  - Nairobi Full Day Excursion Tour
  - Maasai Magic Cultural Tour (Kiserian)

### 2. **Kenyan Multi-Day Bush Safaris**
- **Slug**: `kenyan-multiday-safaris`
- **Description**: Multi-day safari packages within Kenya (excluding Nairobi day trips)
- **Purpose**: For all multi-day safari experiences in Kenyan national parks and reserves
- **Examples**:
  - 4 Days & 3 Nights Maasai Mara Spectacular Getaway
  - 3 Days & 2 Nights Amboseli Spectacular Escapade
  - 3 Days & 2 Nights Ol Pejeta Conservancy Spectacular Escapade
  - Ultimate Kenya Safari Adventure (7 days)

### 3. **Outbound Packages**
- **Slug**: `outbound-packages`
- **Description**: International packages and tours outside Kenya
- **Purpose**: For all travel packages to destinations outside Kenya
- **Examples**:
  - Rwanda Gorilla Trekking Experience
  - Uganda Gorilla and Wildlife Safari
  - Tanzania Great Migration Safari
  - Best of Cape Town Package

---

## Categorization Logic

The system automatically assigns packages to categories based on:

1. **Destination Location**:
   - Checks if the destination is in Kenya or international
   - Identifies Nairobi-specific destinations

2. **Package Duration**:
   - 1-day packages → Nairobi Excursions (if in Nairobi/Kenya)
   - Multi-day packages → Kenyan Multi-Day Safaris (if in Kenya)
   - Any duration → Outbound Packages (if international)

3. **Hierarchical Destination Check**:
   - The system checks the destination hierarchy (Country → City → Place)
   - Automatically identifies Kenya-based destinations even if not explicitly named

---

## Management Command

### Command: `update_package_categories`

Updates package categories in the database.

#### Basic Usage

```bash
# Development database (dry run)
python manage.py update_package_categories --dry-run

# Development database (apply changes)
python manage.py update_package_categories

# Production database (dry run)
DJANGO_ENV=production python manage.py update_package_categories --dry-run

# Production database (apply changes)
DJANGO_ENV=production python manage.py update_package_categories
```

#### Command Options

- `--dry-run`: Preview changes without committing to database
- No additional flags needed for live mode (will prompt for confirmation)

#### What the Command Does

1. **Creates/Updates Categories**: Creates the 3 package categories if they don't exist
2. **Analyzes Packages**: Examines all existing packages in the database
3. **Assigns Categories**: Intelligently assigns each package to the appropriate category
4. **Generates Log**: Creates a detailed JSON log file with all changes
5. **Provides Summary**: Shows statistics of packages processed and categorized

---

## Helper Script

### Script: `scripts/update_package_categories.sh`

Convenient wrapper script for running the management command.

#### Usage Examples

```bash
# Preview changes (dry run) - Development
./scripts/update_package_categories.sh --dry-run

# Update development database
./scripts/update_package_categories.sh

# Preview production changes
./scripts/update_package_categories.sh --production --dry-run

# Update production database
./scripts/update_package_categories.sh --production
```

#### Script Features

- ✅ Color-coded output for better readability
- ✅ Confirmation prompts for production changes
- ✅ Automatic environment detection
- ✅ Safety checks and error handling
- ✅ Usage examples displayed after execution

---

## Database Schema

### PackageCategory Model

```python
class PackageCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Package Model Update

The `Package` model now includes:

```python
category = models.ForeignKey(
    PackageCategory,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='packages'
)
```

---

## Admin Interface

### PackageCategory Admin

Access at: `/admin/adminside/packagecategory/`

**Features**:
- List view shows: name, slug, package count, display order, active status
- Inline editing of display order and active status
- Search by name and description
- Auto-populated slug from name
- Collapsible system information section

### Package Admin Updates

The Package admin now includes:
- Category field in the "Basic Information" section
- Category filter in the list view
- Category column in the package list

---

## Production Deployment Results

### Execution Summary (October 20, 2025)

**Database**: Production PostgreSQL (Supabase)

**Results**:
- ✅ 3 categories created successfully
- ✅ 13 packages processed
- ✅ 13 packages reassigned to categories
- ✅ 0 packages requiring manual review

**Category Distribution**:
- Nairobi Excursions: 4 packages
- Kenyan Multi-Day Bush Safaris: 4 packages
- Outbound Packages: 5 packages

**Log File**: `package_category_changes_20251020_175656.json`

---

## Change Log Files

Each execution of the command generates a detailed JSON log file:

**Filename Format**: `package_category_changes_YYYYMMDD_HHMMSS.json`

**Contents**:
```json
{
  "categories_created": [...],
  "packages_reassigned": [
    {
      "package_name": "...",
      "package_slug": "...",
      "old_category": "...",
      "new_category": "...",
      "destination": "...",
      "duration_days": ...,
      "reason": "..."
    }
  ],
  "packages_unchanged": [...],
  "packages_set_to_null": [...],
  "timestamp": "..."
}
```

---

## Troubleshooting

### Issue: Categories not appearing in admin

**Solution**: Clear browser cache and refresh the admin page

### Issue: Packages assigned to wrong category

**Solution**: 
1. Check the destination hierarchy in the database
2. Manually update the package category in the admin interface
3. Or update the categorization logic in the management command

### Issue: Migration errors

**Solution**:
```bash
# Check migration status
python manage.py showmigrations adminside

# Apply migrations
python manage.py migrate adminside
```

### Issue: Permission denied on script

**Solution**:
```bash
chmod +x scripts/update_package_categories.sh
```

---

## Future Enhancements

Potential improvements to consider:

1. **Frontend Integration**: Display packages grouped by category on the website
2. **Category Pages**: Create dedicated landing pages for each category
3. **Filtering**: Add category-based filtering on package list pages
4. **SEO**: Optimize category pages for search engines
5. **Analytics**: Track which categories are most popular with users

---

## Technical Details

### Files Modified/Created

**Models**:
- `adminside/models.py` - Added `PackageCategory` model and `category` field to `Package`

**Admin**:
- `adminside/admin.py` - Added `PackageCategoryAdmin` and updated `PackageAdmin`

**Migrations**:
- `adminside/migrations/0009_packagecategory_package_category_and_more.py`

**Management Commands**:
- `adminside/management/commands/update_package_categories.py`

**Scripts**:
- `scripts/update_package_categories.sh`

**Documentation**:
- `PACKAGE_CATEGORIES_GUIDE.md` (this file)

### Database Indexes

The following indexes were created for performance:
- `PackageCategory`: slug, is_active
- `Package`: category + status (composite index)

---

## Support

For issues or questions about the package categorization system:

1. Check this documentation first
2. Review the change log files for execution history
3. Test changes in development before applying to production
4. Always use `--dry-run` flag first when making changes

---

**Last Updated**: October 20, 2025  
**Version**: 1.0  
**Author**: Mbugani Luxe Adventures Development Team

