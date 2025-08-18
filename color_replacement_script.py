#!/usr/bin/env python3
"""
Automated Color Replacement Script for Mbugani Luxe Adventures Rebranding
"""

import os
import re
import glob

# Color mapping: Current Novustell → New Mbugani
COLOR_MAPPING = {
    '#5d0000': '[NEW_PRIMARY_COLOR]',      # Mbugani Burgundy → New Primary
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
    
    print(f"\n📊 REPLACEMENT SUMMARY")
    print("=" * 60)
    print(f"Total files updated: {total_files}")
    print(f"Total replacements made: {total_replacements}")

if __name__ == "__main__":
    main()
