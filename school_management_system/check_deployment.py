#!/usr/bin/env python
"""
Script to check if the College Management System is deployed and running correctly.
"""
import argparse
import json
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

def check_endpoint(url, endpoint, expected_status=200, timeout=5):
    """Check if an endpoint is accessible and returns the expected status."""
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    print(f"Checking {full_url}...")
    
    try:
        start_time = time.time()
        response = urlopen(full_url, timeout=timeout)
        elapsed_time = time.time() - start_time
        
        status = response.status
        content = response.read().decode('utf-8')
        
        if status == expected_status:
            print(f"✅ {endpoint} - Status: {status} - Response time: {elapsed_time:.2f}s")
            try:
                # Try to parse JSON response
                json_content = json.loads(content)
                print(f"   Response: {json_content}")
            except json.JSONDecodeError:
                # If not JSON, print a summary
                content_preview = content[:100] + "..." if len(content) > 100 else content
                print(f"   Response: {content_preview}")
            return True
        else:
            print(f"❌ {endpoint} - Expected status {expected_status}, got {status}")
            return False
    except URLError as e:
        print(f"❌ {endpoint} - Error: {e}")
        return False
    except Exception as e:
        print(f"❌ {endpoint} - Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Check College Management System deployment')
    parser.add_argument('url', help='Base URL of the deployed application (e.g., https://college-management-system.onrender.com)')
    args = parser.parse_args()
    
    base_url = args.url
    
    print(f"Checking College Management System deployment at {base_url}")
    print("=" * 60)
    
    # Define endpoints to check
    endpoints = [
        # Basic endpoints
        ("", 200),  # Root endpoint
        ("api", 200),  # API root
        ("docs", 200),  # API documentation
        
        # API endpoints
        ("api/v1/users/me", 401),  # Should return 401 Unauthorized if not authenticated
    ]
    
    success_count = 0
    for endpoint, expected_status in endpoints:
        if check_endpoint(base_url, endpoint, expected_status):
            success_count += 1
    
    print("=" * 60)
    print(f"Results: {success_count}/{len(endpoints)} checks passed")
    
    if success_count == len(endpoints):
        print("✅ Deployment check successful! The application is running correctly.")
        return 0
    else:
        print("❌ Some checks failed. Please check the logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
