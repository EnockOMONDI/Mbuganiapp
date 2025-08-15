#!/usr/bin/env python3
"""
Bulk domain replacement script for rebranding
"""

import os
import re
import glob

def replace_domains_in_file(file_path, replacements):
    """Replace domains in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_domain, new_domain in replacements.items():
            content = content.replace(old_domain, new_domain)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    # Domain replacements mapping
    replacements = {
        "https://www.novustelltravel.com": "https://www.mbuganiluxeadventures.com",
        "https://novustelltravel.com": "https://mbuganiluxeadventures.com",
        "https://wwww.novustelltravel.com": "https://www.mbuganiluxeadventures.com",  # Fix typo too
        "www.novustelltravel.com": "www.mbuganiluxeadventures.com",
        "novustelltravel.onrender.com": "mbuganiapp.onrender.com",
        "novustelltravel.com": "mbuganiluxeadventures.com"
    }
    
    # File patterns to search
    patterns = [
        "*.yaml",
        "*.yml", 
        "*.py",
        "*.html",
        "*.env",
        "**/*.yaml",
        "**/*.yml",
        "**/*.py",
        "**/*.html",
        "**/*.env"
    ]
    
    updated_files = []
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain files
            if any(skip in file_path for skip in ['env/', '__pycache__/', '.pyc', '.sqlite3', '.json', 'update_emails_bulk.py', 'update_domains_bulk.py']):
                continue
                
            if replace_domains_in_file(file_path, replacements):
                updated_files.append(file_path)
    
    print(f"\n📊 Summary: Updated {len(updated_files)} files")
    for file_path in updated_files:
        print(f"   - {file_path}")
    
    print(f"\n🔄 Applied {len(replacements)} domain replacements:")
    for old, new in replacements.items():
        print(f"   {old} → {new}")

if __name__ == "__main__":
    main()
