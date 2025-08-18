#!/usr/bin/env python3
"""
Comprehensive Branding Analysis Tool
Analyzes current Novustell branding elements for Mbugani Luxe Adventures rebranding
"""

import os
import re
import glob
from collections import defaultdict

def analyze_color_usage():
    """Analyze color usage across CSS files"""
    print("🎨 ANALYZING COLOR USAGE")
    print("=" * 50)
    
    color_patterns = {
        'Novustell Blue': r'#5d0000',
        'Novustell Orange': r'#ff9d00',
        'Dark Text': r'#1[CD]231F',
        'Gray Text': r'#484848',
        'Light Background': r'#f[08]f[39]f[cf]',
        'White': r'#ffffff',
        'Other Colors': r'#[0-9a-fA-F]{3,6}'
    }
    
    css_files = glob.glob('**/*.css', recursive=True)
    color_usage = defaultdict(list)
    
    for css_file in css_files:
        if any(skip in css_file for skip in ['env/', '__pycache__/', 'node_modules/']):
            continue
            
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for color_name, pattern in color_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    color_usage[color_name].extend([(css_file, len(matches))])
                    
        except Exception as e:
            print(f"Error reading {css_file}: {e}")
    
    for color_name, files in color_usage.items():
        if files:
            print(f"\n{color_name}:")
            for file_path, count in files:
                print(f"  - {file_path}: {count} instances")
    
    return color_usage

def analyze_logo_assets():
    """Analyze logo and image assets"""
    print("\n🖼️ ANALYZING LOGO & IMAGE ASSETS")
    print("=" * 50)
    
    # Find logo-related files
    logo_patterns = ['*logo*', '*brand*', '*novustell*', '*favicon*']
    logo_files = []
    
    for pattern in logo_patterns:
        logo_files.extend(glob.glob(f'**/{pattern}', recursive=True))
    
    # Remove duplicates and filter
    logo_files = list(set(logo_files))
    logo_files = [f for f in logo_files if not any(skip in f for skip in ['env/', '__pycache__/', '.git/'])]
    
    print("Logo and branding files found:")
    for logo_file in sorted(logo_files):
        if os.path.isfile(logo_file):
            size = os.path.getsize(logo_file)
            print(f"  - {logo_file} ({size:,} bytes)")
    
    return logo_files

def analyze_template_references():
    """Analyze template files for brand references"""
    print("\n📝 ANALYZING TEMPLATE BRAND REFERENCES")
    print("=" * 50)
    
    brand_terms = ['novustell', 'Novustell', 'NOVUSTELL']
    template_files = glob.glob('**/*.html', recursive=True)
    
    brand_references = defaultdict(list)
    
    for template_file in template_files:
        if any(skip in template_file for skip in ['env/', '__pycache__/', 'node_modules/']):
            continue
            
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                for term in brand_terms:
                    if term in line:
                        brand_references[template_file].append((line_num, line.strip()))
                        
        except Exception as e:
            print(f"Error reading {template_file}: {e}")
    
    for template_file, references in brand_references.items():
        print(f"\n{template_file}:")
        for line_num, line in references:
            print(f"  Line {line_num}: {line[:100]}...")
    
    return brand_references

def analyze_static_file_structure():
    """Analyze static file directory structure"""
    print("\n📁 ANALYZING STATIC FILE STRUCTURE")
    print("=" * 50)
    
    static_dirs = ['static/', 'staticfiles/']
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            print(f"\n{static_dir} structure:")
            for root, dirs, files in os.walk(static_dir):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in ['env', '__pycache__', 'node_modules']]
                
                level = root.replace(static_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                
                # Show important files
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    if any(ext in file.lower() for ext in ['.png', '.jpg', '.svg', '.ico', '.css']):
                        if level < 3:  # Limit depth
                            print(f"{subindent}{file}")

def generate_replacement_script():
    """Generate color replacement script template"""
    print("\n🔧 GENERATING REPLACEMENT SCRIPT TEMPLATE")
    print("=" * 50)
    
    script_content = '''#!/usr/bin/env python3
"""
Automated Color Replacement Script for Mbugani Luxe Adventures Rebranding
"""

import os
import re
import glob

# Color mapping: Current Novustell → New Mbugani
COLOR_MAPPING = {
    '#5d0000': '[NEW_PRIMARY_COLOR]',      # Novustell Blue → New Primary
    '#ff9d00': '[NEW_ACCENT_COLOR]',       # Novustell Orange → New Accent
    '#1C231F': '[NEW_TEXT_COLOR]',         # Dark Text → New Text
    '#1D231F': '[NEW_TEXT_COLOR]',         # Dark Text Variant → New Text
    '#484848': '[NEW_SECONDARY_TEXT]',     # Gray Text → New Secondary Text
    '#f8f3fc': '[NEW_LIGHT_BG]',          # Light Background → New Light BG
    '#f0f9ff': '[NEW_LIGHT_BG_ALT]',      # Light Background Alt → New Light BG Alt
}

def replace_colors_in_file(file_path):
    """Replace colors in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        for old_color, new_color in COLOR_MAPPING.items():
            if old_color in content:
                count = content.count(old_color)
                content = content.replace(old_color, new_color)
                replacements_made += count
                print(f"   - {old_color} → {new_color}: {count} times")
        
        if replacements_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path} ({replacements_made} replacements)")
            return replacements_made
        
        return 0
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return 0

def main():
    """Main color replacement function"""
    print("🎨 MBUGANI LUXE ADVENTURES COLOR REPLACEMENT")
    print("=" * 60)
    print("⚠️  IMPORTANT: Update COLOR_MAPPING with actual new colors before running!")
    print()
    
    # File patterns to update
    file_patterns = ['**/*.css', '**/*.html']
    
    total_files = 0
    total_replacements = 0
    
    for pattern in file_patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain directories
            if any(skip in file_path for skip in ['env/', '__pycache__/', 'node_modules/']):
                continue
            
            replacements = replace_colors_in_file(file_path)
            if replacements > 0:
                total_files += 1
                total_replacements += replacements
    
    print(f"\\n📊 REPLACEMENT SUMMARY")
    print("=" * 60)
    print(f"Total files updated: {total_files}")
    print(f"Total replacements made: {total_replacements}")

if __name__ == "__main__":
    main()
'''
    
    with open('color_replacement_script.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created: color_replacement_script.py")
    print("⚠️  Remember to update COLOR_MAPPING with actual new colors!")

def main():
    """Main analysis function"""
    print("🔍 COMPREHENSIVE BRANDING ANALYSIS")
    print("=" * 60)
    print("Analyzing current Novustell branding for Mbugani Luxe Adventures rebranding")
    print()
    
    # Run all analyses
    color_usage = analyze_color_usage()
    logo_files = analyze_logo_assets()
    brand_references = analyze_template_references()
    analyze_static_file_structure()
    generate_replacement_script()
    
    # Summary
    print("\n📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Color instances found: {sum(len(files) for files in color_usage.values())}")
    print(f"Logo/brand files found: {len(logo_files)}")
    print(f"Templates with brand references: {len(brand_references)}")
    print()
    print("✅ Analysis complete! Review the comprehensive_rebranding_plan.md for next steps.")

if __name__ == "__main__":
    main()
