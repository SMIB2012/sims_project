#!/usr/bin/env python3
"""
Test script to analyze user creation forms and identify issues.
"""

import os
import sys
import django

# Setup Django
sys.path.append(r'D:\PMC\sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims.settings')
django.setup()

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

def test_admin_form_access():
    """Test Django admin user creation form"""
    print("🔍 TESTING ADMIN USER CREATION FORM")
    print("=" * 60)

    client = Client()

    # Create admin user for testing
    admin_user = User.objects.create_user(
        username='test_admin',
        email='admin@test.com',
        password='testpass123',
        role='admin',
        first_name='Test',
        last_name='Admin'
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    # Login as admin
    client.login(username='test_admin', password='testpass123')

    # Test admin form access
    admin_add_url = reverse('admin:users_user_add')
    print(f"📋 Admin add URL: {admin_add_url}")

    try:
        response = client.get(admin_add_url)
        print(f"✅ Admin form access: Status {response.status_code}")

        if response.status_code == 200:
            print("✅ Admin form loads successfully")
            # Check for key form fields
            form_content = response.content.decode()
            required_fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role']

            for field in required_fields:
                if f'name="{field}"' in form_content or f'id="id_{field}"' in form_content:
                    print(f"✅ Field '{field}': Present")
                else:
                    print(f"❌ Field '{field}': Missing")

        else:
            print(f"❌ Admin form failed to load: {response.status_code}")

    except Exception as e:
        print(f"❌ Error accessing admin form: {e}")

def test_custom_form_access():
    """Test custom user creation form"""
    print(f"\n🔍 TESTING CUSTOM USER CREATION FORM")
    print("=" * 60)

    client = Client()

    # Create admin user for testing
    admin_user = User.objects.create_user(
        username='test_admin2',
        email='admin2@test.com',
        password='testpass123',
        role='admin',
        first_name='Test',
        last_name='Admin'
    )

    # Login as admin
    client.login(username='test_admin2', password='testpass123')

    # Test custom form access
    custom_add_url = reverse('users:user_create')
    print(f"📋 Custom add URL: {custom_add_url}")

    try:
        response = client.get(custom_add_url)
        print(f"✅ Custom form access: Status {response.status_code}")

        if response.status_code == 200:
            print("✅ Custom form loads successfully")
            # Check for key form fields
            form_content = response.content.decode()
            required_fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role']

            for field in required_fields:
                if f'name="{field}"' in form_content or f'id="{field}"' in form_content:
                    print(f"✅ Field '{field}': Present")
                else:
                    print(f"❌ Field '{field}': Missing")

        else:
            print(f"❌ Custom form failed to load: {response.status_code}")

    except Exception as e:
        print(f"❌ Error accessing custom form: {e}")

def compare_forms():
    """Compare the two forms to identify differences"""
    print(f"\n📊 FORM COMPARISON & RECOMMENDATIONS")
    print("=" * 60)

    print("🔧 Django Admin Form:")
    print("   ✅ Built-in validation")
    print("   ✅ Automatic field generation")
    print("   ✅ Permission handling")
    print("   ❌ Limited customization")
    print("   ❌ Basic UI/UX")

    print(f"\n🎨 Custom Form:")
    print("   ✅ Full UI/UX control")
    print("   ✅ Role-specific features")
    print("   ✅ Better user experience")
    print("   ❌ Manual validation required")
    print("   ❌ More maintenance overhead")

    print(f"\n💡 RECOMMENDATION:")
    print("   • Enhanced Django Admin form with custom templates")
    print("   • Redirect admin user creation to custom form")
    print("   • Keep one unified user creation workflow")

def test_form_functionality():
    """Test actual form submission"""
    print(f"\n🧪 TESTING FORM FUNCTIONALITY")
    print("=" * 60)

    client = Client()

    # Create admin user
    admin_user = User.objects.create_user(
        username='func_test_admin',
        email='func_admin@test.com',
        password='testpass123',
        role='admin',
        first_name='Func',
        last_name='Admin'
    )

    client.login(username='func_test_admin', password='testpass123')

    # Test custom form submission
    form_data = {
        'username': 'test_user_custom',
        'email': 'test_custom@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'pg',
        'specialty': 'medicine',
        'year': '1',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }

    try:
        response = client.post(reverse('users:user_create'), form_data, follow=True)

        if User.objects.filter(username='test_user_custom').exists():
            print("✅ Custom form: User created successfully")
        else:
            print("❌ Custom form: User creation failed")

        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        if messages:
            for message in messages:
                print(f"📝 Message: {message}")

    except Exception as e:
        print(f"❌ Custom form error: {e}")

if __name__ == "__main__":
    print("🚀 USER CREATION FORMS ANALYSIS")
    print("Analyzing both Django admin and custom user creation forms")
    print("=" * 80)

    test_admin_form_access()
    test_custom_form_access()
    compare_forms()
    test_form_functionality()

    print(f"\n✨ Analysis completed!")
    print("💡 Check the analysis above for recommended consolidation approach")
