#!/usr/bin/env python3
"""
Script to replace "Novustell Travel <novustellke@gmail.com>" with "Mbugani Luxe Adventures <novustellke@gmail.com>"
"""

import os
import glob

def replace_email_branding_in_file(file_path):
    """Replace email branding in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_string = "Novustell Travel <novustellke@gmail.com>"
        new_string = "Mbugani Luxe Adventures <novustellke@gmail.com>"
        
        # Count occurrences before replacement
        count = content.count(old_string)
        
        if count > 0:
            new_content = content.replace(old_string, new_string)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated: {file_path} ({count} instances)")
            return count
        else:
            return 0
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return 0

def main():
    old_string = "Novustell Travel <novustellke@gmail.com>"
    new_string = "Mbugani Luxe Adventures <novustellke@gmail.com>"
    
    print("🔍 SEARCHING FOR EMAIL BRANDING INSTANCES")
    print("=" * 60)
    print(f"Old: {old_string}")
    print(f"New: {new_string}")
    print()
    
    # File patterns to search
    patterns = [
        "*.env",
        "*.py",
        "*.html",
        "*.yaml",
        "*.yml",
        "*.md",
        "*.txt",
        "**/*.env",
        "**/*.py", 
        "**/*.html",
        "**/*.yaml",
        "**/*.yml",
        "**/*.md",
        "**/*.txt"
    ]
    
    updated_files = []
    total_instances = 0
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain directories and files
            if any(skip in file_path for skip in ['env/', '__pycache__/', '.pyc', '.sqlite3', 'replace_email_branding.py']):
                continue
            
            instances = replace_email_branding_in_file(file_path)
            if instances > 0:
                updated_files.append((file_path, instances))
                total_instances += instances
    
    print("\n📊 REPLACEMENT SUMMARY")
    print("=" * 60)
    print(f"Total files updated: {len(updated_files)}")
    print(f"Total instances replaced: {total_instances}")
    print()
    
    if updated_files:
        print("📁 FILES MODIFIED:")
        for file_path, count in updated_files:
            print(f"   - {file_path}: {count} instance(s)")
    else:
        print("ℹ️  No files needed updating")
    
    print(f"\n✅ Email branding replacement completed!")
    print(f"   Brand name updated while preserving email address: novustellke@gmail.com")

if __name__ == "__main__":
    main()
