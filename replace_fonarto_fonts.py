#!/usr/bin/env python3
"""
Script to replace Fonarto font references with TAN-Garland-Regular font
"""

import os
import glob
import re

def replace_fonarto_in_file(file_path):
    """Replace Fonarto font references in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        # Font family replacements
        font_replacements = {
            # Basic font-family declarations
            "font-family: 'Fonarto', sans-serif;": "font-family: 'TAN-Garland-Regular', sans-serif;",
            "font-family: 'Fonarto',": "font-family: 'TAN-Garland-Regular',",
            "font-family: 'Fonarto'": "font-family: 'TAN-Garland-Regular'",
            
            # @font-face declarations
            "font-family: 'Fonarto';": "font-family: 'TAN-Garland-Regular';",
            "font-family: 'Fonarto Regular';": "font-family: 'TAN-Garland-Regular';",
            "font-family: 'Fonarto Light';": "font-family: 'TAN-Garland-Light';",
            "font-family: 'Fonarto Bold';": "font-family: 'TAN-Garland-Bold';",
            
            # Local font references
            "local('Fonarto Regular')": "local('TAN-Garland-Regular')",
            "local('Fonarto Light')": "local('TAN-Garland-Light')",
            "local('Fonarto Bold')": "local('TAN-Garland-Bold')",
            "local('Fonarto')": "local('TAN-Garland-Regular')",
            
            # Font loading references
            "'Fonarto'": "'TAN-Garland-Regular'",
            '"Fonarto"': '"TAN-Garland-Regular"',
            
            # Font file references (update to new font files)
            "FonartoRegular-8Mon2.woff": "TAN-Garland-Regular.woff2",
            "FonartoLight-BWxv3.woff": "TAN-Garland-Light.woff2",
            "FonartoBold-RpYOo.woff": "TAN-Garland-Bold.woff2",
            
            # Documentation references
            "Custom Fonarto Fonts": "Custom TAN-Garland Fonts",
            "Fonarto Custom Fonts": "TAN-Garland Custom Fonts",
        }
        
        # Apply replacements
        for old_text, new_text in font_replacements.items():
            if old_text in content:
                count = content.count(old_text)
                content = content.replace(old_text, new_text)
                replacements_made += count
                print(f"   - {old_text} → {new_text}: {count} times")
        
        # Write back if changes were made
        if replacements_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated: {file_path} ({replacements_made} total replacements)")
            return replacements_made
        else:
            return 0
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return 0

def create_font_face_declaration():
    """Create @font-face declaration for TAN-Garland fonts"""
    font_face_css = """
/* TAN-Garland Font Family */
@font-face {
    font-family: 'TAN-Garland-Regular';
    src: url('../fonts/TAN-Garland-Regular.woff2') format('woff2'),
         url('../fonts/TAN-Garland-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'TAN-Garland-Light';
    src: url('../fonts/TAN-Garland-Light.woff2') format('woff2'),
         url('../fonts/TAN-Garland-Light.ttf') format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'TAN-Garland-Bold';
    src: url('../fonts/TAN-Garland-Bold.woff2') format('woff2'),
         url('../fonts/TAN-Garland-Bold.ttf') format('truetype');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}
"""
    return font_face_css

def main():
    print("🔤 REPLACING FONARTO FONTS WITH TAN-GARLAND-REGULAR")
    print("=" * 70)
    print("Updating font references for Mbugani Luxe Adventures rebranding")
    print()
    
    # File patterns to search
    patterns = [
        "**/*.css",
        "**/*.scss",
        "**/*.html",
        "**/*.htm"
    ]
    
    updated_files = []
    total_replacements = 0
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain directories
            if any(skip in file_path for skip in ['env/', '__pycache__/', 'node_modules/', '.git/', 'replace_fonarto_fonts.py']):
                continue
            
            replacements = replace_fonarto_in_file(file_path)
            if replacements > 0:
                updated_files.append((file_path, replacements))
                total_replacements += replacements
    
    print(f"\n📊 REPLACEMENT SUMMARY")
    print("=" * 70)
    print(f"Total files updated: {len(updated_files)}")
    print(f"Total replacements made: {total_replacements}")
    print()
    
    if updated_files:
        print("📁 FILES MODIFIED:")
        for file_path, count in updated_files:
            print(f"   - {file_path}: {count} replacement(s)")
    else:
        print("ℹ️  No files needed updating")
    
    # Create font face CSS file
    print(f"\n🎨 CREATING FONT-FACE DECLARATIONS")
    print("=" * 70)
    
    font_css_path = "static/css/tan-garland-fonts.css"
    try:
        os.makedirs(os.path.dirname(font_css_path), exist_ok=True)
        with open(font_css_path, 'w', encoding='utf-8') as f:
            f.write(create_font_face_declaration())
        print(f"✅ Created: {font_css_path}")
        print("   Include this file in your templates or import it in your main CSS")
    except Exception as e:
        print(f"❌ Error creating font CSS file: {e}")
    
    print(f"\n✅ Font replacement completed!")
    print("📝 Next steps:")
    print("   1. Include the new font CSS file in your templates")
    print("   2. Ensure TAN-Garland font files are in static/fonts/")
    print("   3. Test the new fonts in your application")
    print("   4. Clear browser cache to see changes")

if __name__ == "__main__":
    main()
