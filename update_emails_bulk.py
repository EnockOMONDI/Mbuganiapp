#!/usr/bin/env python3
"""
Bulk email domain replacement script for rebranding
"""

import os
import re
import glob

def replace_emails_in_file(file_path, old_domain, new_domain):
    """Replace email domains in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match emails with the old domain
        pattern = r'([a-zA-Z0-9._%+-]+)@' + re.escape(old_domain)
        replacement = r'\1@' + new_domain
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    old_domain = "novustelltravel.com"
    new_domain = "mbuganiluxeadventures.com"
    
    # File patterns to search
    patterns = [
        "users/**/*.html",
        "users/**/*.py",
        "templates/**/*.html",
        "*.py",
        "**/*.py"
    ]
    
    updated_files = []
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain files
            if any(skip in file_path for skip in ['env/', '__pycache__/', '.pyc', '.sqlite3', '.json']):
                continue
                
            if replace_emails_in_file(file_path, old_domain, new_domain):
                updated_files.append(file_path)
    
    print(f"\n📊 Summary: Updated {len(updated_files)} files")
    for file_path in updated_files:
        print(f"   - {file_path}")

if __name__ == "__main__":
    main()
