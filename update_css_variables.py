#!/usr/bin/env python3
"""
Script to update CSS variables from --novustell-* to --mbugani-*
"""

import os
import glob

def update_css_variables_in_file(file_path):
    """Update CSS variables in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CSS variable replacements
        replacements = {
            'var(--novustell-primary)': 'var(--mbugani-primary)',
            'var(--novustell-secondary)': 'var(--mbugani-secondary)',
            'var(--novustell-light)': 'var(--mbugani-light)',
            'var(--novustell-dark)': 'var(--mbugani-dark)',
            '--novustell-primary': '--mbugani-primary',
            '--novustell-secondary': '--mbugani-secondary',
            '--novustell-light': '--mbugani-light',
            '--novustell-dark': '--mbugani-dark',
            '.novustell-highlight': '.mbugani-highlight',
            '.novustell-primary': '.mbugani-primary'
        }
        
        original_content = content
        total_replacements = 0
        
        # Apply all replacements
        for old_var, new_var in replacements.items():
            count = content.count(old_var)
            if count > 0:
                content = content.replace(old_var, new_var)
                total_replacements += count
                print(f"   - {old_var} → {new_var}: {count} times")
        
        if total_replacements > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated: {file_path} ({total_replacements} total replacements)")
            return total_replacements
        else:
            return 0
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return 0

def main():
    print("🎨 UPDATING CSS VARIABLES")
    print("=" * 60)
    print("Updating --novustell-* variables to --mbugani-*")
    print()
    
    # File patterns to search
    patterns = [
        "**/*.css",
        "**/*.scss",
        "**/*.less"
    ]
    
    updated_files = []
    total_replacements = 0
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain directories
            if any(skip in file_path for skip in ['env/', '__pycache__/', 'node_modules/', 'update_css_variables.py']):
                continue
            
            replacements = update_css_variables_in_file(file_path)
            if replacements > 0:
                updated_files.append((file_path, replacements))
                total_replacements += replacements
    
    print(f"\n📊 REPLACEMENT SUMMARY")
    print("=" * 60)
    print(f"Total files updated: {len(updated_files)}")
    print(f"Total replacements made: {total_replacements}")
    print()
    
    if updated_files:
        print("📁 FILES MODIFIED:")
        for file_path, count in updated_files:
            print(f"   - {file_path}: {count} replacement(s)")
    else:
        print("ℹ️  No files needed updating")
    
    print(f"\n✅ CSS variable update completed!")

if __name__ == "__main__":
    main()
