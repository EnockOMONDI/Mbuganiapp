#!/usr/bin/env python3
"""
Comprehensive rebranding analysis script
"""

import os
import re
import glob
from collections import defaultdict

def analyze_file(file_path, search_terms):
    """Analyze a file for brand references"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        findings = []
        for term in search_terms:
            if term.lower() in content.lower():
                # Count occurrences
                count = len(re.findall(re.escape(term), content, re.IGNORECASE))
                if count > 0:
                    findings.append((term, count))
        
        return findings
    except Exception as e:
        return []

def categorize_file(file_path):
    """Categorize file by type and importance"""
    if any(x in file_path for x in ['settings', 'config', '.env', 'render.yaml']):
        return 'CRITICAL'
    elif any(x in file_path for x in ['templates', 'static', 'css', 'js']):
        return 'IMPORTANT'
    elif any(x in file_path for x in ['test', 'doc', 'readme']):
        return 'OPTIONAL'
    else:
        return 'IMPORTANT'

def main():
    # Brand terms to search for
    search_terms = [
        'Novustell',
        'NOVUSTELL', 
        'novustell',
        'Novustell Travel',
        'NOVUSTELL TRAVEL',
        'novustell-travel',
        'novustellke@gmail.com'
    ]
    
    # File patterns to search
    patterns = [
        "*.py", "*.html", "*.css", "*.js", "*.yaml", "*.yml", "*.env", "*.md", "*.txt",
        "**/*.py", "**/*.html", "**/*.css", "**/*.js", "**/*.yaml", "**/*.yml", "**/*.env", "**/*.md", "**/*.txt"
    ]
    
    findings_by_category = defaultdict(list)
    total_files = 0
    total_references = 0
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            # Skip certain files
            if any(skip in file_path for skip in ['env/', '__pycache__/', '.pyc', '.sqlite3', '.json', 'update_', 'rebranding_analysis.py']):
                continue
            
            findings = analyze_file(file_path, search_terms)
            if findings:
                category = categorize_file(file_path)
                total_files += 1
                file_total = sum(count for _, count in findings)
                total_references += file_total
                
                findings_by_category[category].append({
                    'file': file_path,
                    'findings': findings,
                    'total': file_total
                })
    
    # Generate report
    print("🔍 COMPREHENSIVE REBRANDING ANALYSIS REPORT")
    print("=" * 60)
    print(f"📊 Total files with brand references: {total_files}")
    print(f"📊 Total brand references found: {total_references}")
    print()
    
    # Sort categories by priority
    priority_order = ['CRITICAL', 'IMPORTANT', 'OPTIONAL']
    
    for category in priority_order:
        if category in findings_by_category:
            files = findings_by_category[category]
            files.sort(key=lambda x: x['total'], reverse=True)
            
            print(f"🚨 {category} FILES ({len(files)} files)")
            print("-" * 40)
            
            for item in files[:10]:  # Show top 10 files per category
                print(f"📁 {item['file']} ({item['total']} references)")
                for term, count in item['findings']:
                    print(f"   - '{term}': {count} times")
                print()
            
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
                print()
    
    # Specific recommendations
    print("🎯 REBRANDING RECOMMENDATIONS")
    print("=" * 60)
    
    print("📋 CRITICAL PRIORITY:")
    print("- Configuration files (settings.py, .env, render.yaml)")
    print("- Service names and deployment configurations")
    print("- Email templates and automated communications")
    print()
    
    print("📋 IMPORTANT PRIORITY:")
    print("- Website templates and user-facing content")
    print("- CSS/JS files with brand styling")
    print("- Meta tags and SEO content")
    print("- Static assets and images")
    print()
    
    print("📋 OPTIONAL PRIORITY:")
    print("- Test files and documentation")
    print("- Development scripts and utilities")
    print("- Comments and internal references")

if __name__ == "__main__":
    main()
