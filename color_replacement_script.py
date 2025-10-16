#!/usr/bin/env python3
"""
Mbugani Luxe Adventures - Color Replacement Script
Replace all instances of #291c1b with #291c1b across the entire codebase
"""

import os
import re
import glob
from pathlib import Path

# Color mapping
OLD_COLOR = '#291c1b'
NEW_COLOR = '#291c1b'

# Files to exclude (binary files, logs, etc.)
EXCLUDE_PATTERNS = [
    '*.pyc',
    '*.pyo',
    '*.log',
    '*.sqlite3',
    '*.db',
    '*.jpg',
    '*.jpeg',
    '*.png',
    '*.gif',
    '*.bmp',
    '*.ico',
    '*.svg',  # SVG files might have binary content
    '*.woff',
    '*.woff2',
    '*.ttf',
    '*.eot',
    '*.pdf',
    '*.zip',
    '*.tar.gz',
    '*.git*',
    '__pycache__',
    'node_modules',
    '.git',
    'media',
    'staticfiles_dev',
    'staticfiles',
    'logs',
    'status'
]

def is_text_file(filepath):
    """Check if a file is a text file"""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Binary file
                return False
        return True
    except:
        return False

def should_process_file(filepath):
    """Check if file should be processed"""
    # Check exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if filepath.endswith(pattern[1:]):
                return False
        elif pattern in filepath:
            return False

    # Check if it's a text file
    return is_text_file(filepath)

def replace_colors_in_file(filepath):
    """Replace colors in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Count occurrences before replacement
        old_count = content.count(OLD_COLOR)

        if old_count > 0:
            # Replace the color
            new_content = content.replace(OLD_COLOR, NEW_COLOR)

            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return old_count
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

    return 0

def main():
    """Main function"""
    print("Mbugani Luxe Adventures - Color Replacement Script")
    print(f"Replacing {OLD_COLOR} with {NEW_COLOR}")
    print("-" * 60)

    # Get current directory
    base_dir = Path.cwd()

    total_files_processed = 0
    total_replacements = 0

    # Walk through all files
    for filepath in base_dir.rglob('*'):
        if filepath.is_file():
            filepath_str = str(filepath)

            if should_process_file(filepath_str):
                replacements = replace_colors_in_file(filepath_str)
                if replacements > 0:
                    print(f"✅ {filepath_str}: {replacements} replacements")
                    total_files_processed += 1
                    total_replacements += replacements

    print("-" * 60)
    print(f"Summary: {total_replacements} replacements in {total_files_processed} files")
    print("Color replacement completed!")

if __name__ == "__main__":
    main()
