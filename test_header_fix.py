#!/usr/bin/env python
"""
Test script to verify header fix for admin user creation form
=============================================================

This script checks that the admin form template is properly standalone
without the blue header from base.html
"""

import requests
from bs4 import BeautifulSoup

def test_header_fix():
    """Test that only the purple admin header shows up"""
    print("🔍 TESTING HEADER FIX")
    print("=" * 40)

    url = "http://127.0.0.1:8000/users/create/?next=/admin/users/user/"

    try:
        response = requests.get(url, timeout=10, allow_redirects=True)

        if response.status_code == 200:
            print(f"✅ Page loads successfully: {response.status_code}")

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for headers
            admin_headers = soup.find_all(class_='admin-header')
            blue_headers = soup.find_all('nav', class_='navbar')  # Common blue header classes
            base_headers = soup.find_all('header')

            print(f"\n📊 HEADER ANALYSIS:")
            print(f"   Admin headers (purple): {len(admin_headers)}")
            print(f"   Navbar headers (blue): {len(blue_headers)}")
            print(f"   Total header elements: {len(base_headers)}")

            # Check for specific elements
            has_admin_gradient = '--admin-gradient' in response.text
            has_purple_header = 'admin-header' in response.text
            extends_base = '{% extends' in response.text

            print(f"\n🎨 STYLING ANALYSIS:")
            print(f"   Has admin gradient: {'✅' if has_admin_gradient else '❌'}")
            print(f"   Has purple header: {'✅' if has_purple_header else '❌'}")
            print(f"   Extends base template: {'❌' if not extends_base else '⚠️ Still extending!'}")

            # Check page title
            title = soup.find('title')
            title_text = title.text if title else "No title found"
            print(f"   Page title: {title_text}")

            # Success criteria
            success = (
                len(admin_headers) >= 1 and  # Has admin header
                len(blue_headers) == 0 and   # No blue headers
                has_admin_gradient and       # Has admin styling
                not extends_base             # Doesn't extend base
            )

            if success:
                print(f"\n🎉 HEADER FIX SUCCESSFUL!")
                print("   ✅ Only purple admin header is present")
                print("   ✅ No blue header from base template")
                print("   ✅ Admin styling is applied")
                print("   ✅ Template is standalone")
            else:
                print(f"\n⚠️  HEADER ISSUES DETECTED:")
                if len(blue_headers) > 0:
                    print("   ❌ Blue header still present")
                if not has_admin_gradient:
                    print("   ❌ Admin styling missing")
                if extends_base:
                    print("   ❌ Still extending base template")

            return success

        else:
            print(f"❌ Page failed to load: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing page: {e}")
        return False

def show_instructions():
    """Show manual testing instructions"""
    print("\n📝 MANUAL TESTING INSTRUCTIONS:")
    print("=" * 35)
    print("1. Visit: http://127.0.0.1:8000/users/create/?next=/admin/users/user/")
    print("2. Verify you see ONLY the purple admin header")
    print("3. Check that there's no blue header at the top")
    print("4. Confirm the admin styling and gradient background")
    print("5. Test the form functionality")

if __name__ == "__main__":
    success = test_header_fix()
    show_instructions()

    if success:
        print("\n✅ HEADER FIX: COMPLETE")
    else:
        print("\n⚠️  HEADER FIX: NEEDS ATTENTION")
