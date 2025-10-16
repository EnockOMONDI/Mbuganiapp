#!/usr/bin/env python3
"""
Mbugani Luxe Adventures - Gradient Replacement Script
Replace all gradients containing #471601 with #291c1b
"""

import os
import re
import glob
from pathlib import Path

# Pattern to match gradients containing #471601
GRADIENT_PATTERN = r'linear-gradient\([^)]*#471601[^)]*\)'

# Exclude patterns
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

def replace_gradients_in_file(filepath):
    """Replace gradients in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find all gradients containing #471601
        gradients = re.findall(GRADIENT_PATTERN, content)
        replacements_made = 0

        for gradient in gradients:
            # Replace the entire gradient with #291c1b
            new_content = content.replace(gradient, '#291c1b')
            if new_content != content:
                content = new_content
                replacements_made += 1
                print(f"  Replaced: {gradient} -> #291c1b")

        if replacements_made > 0:
            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        return replacements_made
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

def main():
    """Main function"""
    print("Mbugani Luxe Adventures - Gradient Replacement Script")
    print("Replacing all gradients containing #471601 with #291c1b")
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
                replacements = replace_gradients_in_file(filepath_str)
                if replacements > 0:
                    print(f"✅ {filepath_str}: {replacements} replacements")
                    total_files_processed += 1
                    total_replacements += replacements

    print("-" * 60)
    print(f"Summary: {total_replacements} gradient replacements in {total_files_processed} files")
    print("Gradient replacement completed!")

if __name__ == "__main__":
    main()