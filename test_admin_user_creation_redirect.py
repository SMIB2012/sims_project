#!/usr/bin/env python
"""
Test script to verify admin user creation form redirect
"""
import os
import sys
import django
import requests

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_admin_user_creation_redirect():
    """Test that the admin user creation form redirects properly"""
    print("🔍 TESTING ADMIN USER CREATION FORM REDIRECT")
    print("=" * 55)

    base_url = "http://127.0.0.1:8000"

    # Test URLs
    test_cases = [
        {
            "name": "Admin User Add Form",
            "url": f"{base_url}/admin/users/user/add/",
            "expected": "Should redirect to custom user creation form",
            "check_redirect": True
        },
        {
            "name": "Custom User Creation Form",
            "url": f"{base_url}/users/create/",
            "expected": "Should load custom form with all fields",
            "check_redirect": False
        },
        {
            "name": "Custom Form with Admin Context",
            "url": f"{base_url}/users/create/?next=/admin/users/user/",
            "expected": "Should show admin breadcrumbs and context",
            "check_redirect": False
        }
    ]

    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   URL: {test_case['url']}")

        try:
            # Make request with redirect following
            response = requests.get(test_case['url'], timeout=5, allow_redirects=True)

            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code} (OK)")

                # Check for specific content indicators
                content = response.text.lower()

                if test_case['check_redirect']:
                    # For admin form, should redirect to custom form
                    if '/users/create/' in response.url:
                        print(f"   ✅ Redirect: Successfully redirected to custom form")
                    else:
                        print(f"   ❌ Redirect: Not redirected properly (final URL: {response.url})")

                # Check for form elements that indicate comprehensive form
                form_elements = [
                    'role-card',  # Role selection cards
                    'specialty',  # Specialty field
                    'supervisor', # Supervisor selection
                    'password1',  # Password field
                    'phone_number', # Additional fields
                    'registration_number'
                ]

                found_elements = [elem for elem in form_elements if elem in content]
                print(f"   📝 Form Elements Found: {len(found_elements)}/{len(form_elements)}")

                if len(found_elements) >= 4:
                    print(f"   ✅ Form: Comprehensive form detected")
                else:
                    print(f"   ⚠️  Form: Limited form elements detected")

                # Check for admin context if applicable
                if 'next=/admin/' in test_case['url']:
                    if 'breadcrumb' in content or 'admin interface' in content:
                        print(f"   ✅ Context: Admin context detected")
                    else:
                        print(f"   ⚠️  Context: Admin context not detected")

            elif response.status_code == 302:
                print(f"   ✅ Status: {response.status_code} (Redirect)")
                print(f"   📍 Redirects to: {response.headers.get('Location', 'Unknown')}")
            else:
                print(f"   ❌ Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 55)
    print("🎯 SUMMARY:")
    print("   - Admin form should redirect to enhanced custom form")
    print("   - Custom form should have all user creation fields")
    print("   - Admin context should show breadcrumbs and proper navigation")
    print("   - All form elements should be present for comprehensive user creation")

    print("\n✨ If all tests pass, the admin user creation form is working correctly!")

if __name__ == "__main__":
    test_admin_user_creation_redirect()
