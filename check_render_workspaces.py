#!/usr/bin/env python3
"""
Script to check Render workspaces using the Render API
This helps verify your API key and list available workspaces
"""

import requests
import json
import os
from typing import Dict, List, Optional

def check_render_workspaces(api_key: str) -> Optional[List[Dict]]:
    """
    Check Render workspaces using the API
    
    Args:
        api_key: Your Render API key
        
    Returns:
        List of workspaces or None if error
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔍 Checking Render workspaces...")
        response = requests.get(
            'https://api.render.com/v1/owners',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            workspaces = response.json()
            print(f"✅ Successfully retrieved {len(workspaces)} workspace(s)")
            return workspaces
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API key")
            return None
        elif response.status_code == 403:
            print("❌ Access forbidden - check API key permissions")
            return None
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def check_render_services(api_key: str) -> Optional[List[Dict]]:
    """
    Check Render services using the API
    
    Args:
        api_key: Your Render API key
        
    Returns:
        List of services or None if error
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔍 Checking Render services...")
        response = requests.get(
            'https://api.render.com/v1/services',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            services = response.json()
            print(f"✅ Successfully retrieved {len(services)} service(s)")
            return services
        else:
            print(f"❌ Services API request failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking services: {e}")
        return None

def display_workspaces(workspaces: List[Dict]) -> None:
    """Display workspace information in a readable format"""
    print("\n" + "="*60)
    print("📋 RENDER WORKSPACES")
    print("="*60)
    
    for i, workspace in enumerate(workspaces, 1):
        print(f"\n{i}. Workspace: {workspace.get('name', 'Unknown')}")
        print(f"   ID: {workspace.get('id', 'Unknown')}")
        print(f"   Type: {workspace.get('type', 'Unknown')}")
        print(f"   Email: {workspace.get('email', 'Unknown')}")
        
        if 'createdAt' in workspace:
            print(f"   Created: {workspace['createdAt']}")

def display_services(services: List[Dict]) -> None:
    """Display service information in a readable format"""
    print("\n" + "="*60)
    print("🚀 RENDER SERVICES")
    print("="*60)
    
    for i, service in enumerate(services, 1):
        print(f"\n{i}. Service: {service.get('name', 'Unknown')}")
        print(f"   ID: {service.get('id', 'Unknown')}")
        print(f"   Type: {service.get('type', 'Unknown')}")
        print(f"   Status: {service.get('serviceDetails', {}).get('status', 'Unknown')}")
        print(f"   URL: {service.get('serviceDetails', {}).get('url', 'N/A')}")
        print(f"   Region: {service.get('serviceDetails', {}).get('region', 'Unknown')}")

def main():
    """Main function to check Render account information"""
    print("🌟 Render Account Information Checker")
    print("="*50)
    
    # Try to get API key from environment variable first
    api_key = os.getenv('RENDER_API_KEY')
    
    if not api_key:
        print("\n📝 Please provide your Render API key:")
        print("   You can get this from: https://dashboard.render.com/account/api-keys")
        api_key = input("   Enter API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Check workspaces
    workspaces = check_render_workspaces(api_key)
    if workspaces:
        display_workspaces(workspaces)
    
    # Check services
    services = check_render_services(api_key)
    if services:
        display_services(services)
    
    print("\n" + "="*60)
    print("🔧 MCP SERVER SETUP INSTRUCTIONS")
    print("="*60)
    print("\nTo use this with MCP servers, configure your AI tool with:")
    print(f"   URL: https://mcp.render.com/mcp")
    print(f"   Header: Authorization: Bearer {api_key[:8]}...")
    print("\nFor Augment Code:")
    print("   1. Open VS Code with Augment extension")
    print("   2. Click gear icon → Settings")
    print("   3. Add remote MCP server with above details")
    print("\nFor more details, see: https://render.com/docs/mcp-server")

if __name__ == "__main__":
    main()
