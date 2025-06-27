#!/usr/bin/env python3
"""
Test script to verify user creation form consolidation and functionality.
"""

import os
import sys
import django

# Setup Django
sys.path.append(r'D:\PMC\sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

def setup_test_admin():
    """Create admin user for testing"""
    # Clean up any existing test users
    User.objects.filter(username__startswith='test_').delete()

    admin_user = User.objects.create_user(
        username='test_admin_consolidation',
        email='admin_consolidation@test.com',
        password='testpass123',
        role='admin',
        first_name='Test',
        last_name='Admin'
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    return admin_user

def test_admin_redirect():
    """Test that admin user creation redirects to custom form"""
    print("🔍 TESTING ADMIN FORM REDIRECT")
    print("=" * 50)

    client = Client()
    admin_user = setup_test_admin()
    client.login(username='test_admin_consolidation', password='testpass123')

    try:
        # Access admin add form
        admin_url = reverse('admin:users_user_add')
        response = client.get(admin_url)

        print(f"📋 Admin URL: {admin_url}")
        print(f"✅ Response Status: {response.status_code}")

        if response.status_code == 200:
            content = response.content.decode()
            if 'Enhanced User Creation Form' in content:
                print("✅ Admin form shows redirect message")
            if 'users:user_create' in content:
                print("✅ Admin form contains link to custom form")

    except Exception as e:
        print(f"❌ Error testing admin redirect: {e}")

def test_custom_form_functionality():
    """Test custom form with various user types"""
    print(f"\n🧪 TESTING CUSTOM FORM FUNCTIONALITY")
    print("=" * 50)

    client = Client()
    admin_user = setup_test_admin()
    client.login(username='test_admin_consolidation', password='testpass123')

    # Test creating different user types
    test_cases = [
        {
            'name': 'Admin User',
            'data': {
                'username': 'test_admin_user',
                'email': 'test_admin@example.com',
                'first_name': 'Test',
                'last_name': 'Admin',
                'role': 'admin',
                'password1': 'testpass123',
                'password2': 'testpass123',
            }
        },
        {
            'name': 'Supervisor User',
            'data': {
                'username': 'test_supervisor_user',
                'email': 'test_supervisor@example.com',
                'first_name': 'Test',
                'last_name': 'Supervisor',
                'role': 'supervisor',
                'specialty': 'medicine',
                'password1': 'testpass123',
                'password2': 'testpass123',
            }
        }
    ]

    for test_case in test_cases:
        try:
            print(f"\n📝 Testing {test_case['name']}:")

            response = client.post(reverse('users:user_create'), test_case['data'], follow=True)

            # Check if user was created
            username = test_case['data']['username']
            user_created = User.objects.filter(username=username).exists()

            if user_created:
                print(f"✅ {test_case['name']}: Created successfully")
                created_user = User.objects.get(username=username)
                print(f"   Role: {created_user.role}")
                print(f"   Email: {created_user.email}")
            else:
                print(f"❌ {test_case['name']}: Creation failed")

                # Check for error messages
                messages = list(get_messages(response.wsgi_request))
                if messages:
                    for message in messages:
                        print(f"   Error: {message}")

        except Exception as e:
            print(f"❌ Error testing {test_case['name']}: {e}")

def test_pg_user_with_supervisor():
    """Test PG user creation with supervisor assignment"""
    print(f"\n👨‍⚕️ TESTING PG USER WITH SUPERVISOR")
    print("=" * 50)

    client = Client()
    admin_user = setup_test_admin()
    client.login(username='test_admin_consolidation', password='testpass123')

    try:
        # First create a supervisor
        supervisor_data = {
            'username': 'test_supervisor_for_pg',
            'email': 'supervisor_for_pg@example.com',
            'first_name': 'Test',
            'last_name': 'Supervisor',
            'role': 'supervisor',
            'specialty': 'surgery',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        response = client.post(reverse('users:user_create'), supervisor_data)
        supervisor = User.objects.get(username='test_supervisor_for_pg')
        print(f"✅ Supervisor created: {supervisor.get_display_name()}")

        # Now create a PG with this supervisor
        pg_data = {
            'username': 'test_pg_with_supervisor',
            'email': 'test_pg@example.com',
            'first_name': 'Test',
            'last_name': 'PG',
            'role': 'pg',
            'specialty': 'surgery',
            'year': '2',
            'supervisor_choice': str(supervisor.id),
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        response = client.post(reverse('users:user_create'), pg_data, follow=True)

        if User.objects.filter(username='test_pg_with_supervisor').exists():
            pg_user = User.objects.get(username='test_pg_with_supervisor')
            print(f"✅ PG User created: {pg_user.get_display_name()}")
            print(f"   Specialty: {pg_user.specialty}")
            print(f"   Year: {pg_user.year}")
            print(f"   Supervisor: {pg_user.supervisor.get_display_name() if pg_user.supervisor else 'None'}")
        else:
            print("❌ PG User creation failed")

    except Exception as e:
        print(f"❌ Error testing PG with supervisor: {e}")

def test_form_validation():
    """Test form validation with invalid data"""
    print(f"\n🛡️ TESTING FORM VALIDATION")
    print("=" * 50)

    client = Client()
    admin_user = setup_test_admin()
    client.login(username='test_admin_consolidation', password='testpass123')

    # Test invalid data scenarios
    invalid_cases = [
        {
            'name': 'Missing required fields',
            'data': {
                'username': '',
                'email': '',
                'password1': 'testpass123',
                'password2': 'testpass123',
            }
        },
        {
            'name': 'Password mismatch',
            'data': {
                'username': 'test_password_mismatch',
                'email': 'test_mismatch@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'admin',
                'password1': 'testpass123',
                'password2': 'differentpass',
            }
        },
        {
            'name': 'PG without supervisor',
            'data': {
                'username': 'test_pg_no_supervisor',
                'email': 'test_pg_no_sup@example.com',
                'first_name': 'Test',
                'last_name': 'PG',
                'role': 'pg',
                'specialty': 'medicine',
                'year': '1',
                'password1': 'testpass123',
                'password2': 'testpass123',
            }
        }
    ]

    for case in invalid_cases:
        try:
            print(f"\n📝 Testing {case['name']}:")

            response = client.post(reverse('users:user_create'), case['data'])

            # Check for error messages
            messages = list(get_messages(response.wsgi_request))
            if messages:
                print(f"✅ Validation working - found {len(messages)} error(s)")
                for message in messages[:2]:  # Show first 2 errors
                    print(f"   Error: {message}")
            else:
                print("❌ No validation errors found (unexpected)")

        except Exception as e:
            print(f"❌ Error testing {case['name']}: {e}")

def cleanup_test_users():
    """Clean up test users"""
    print(f"\n🧹 CLEANING UP TEST USERS")
    print("=" * 50)

    test_users = User.objects.filter(username__startswith='test_')
    count = test_users.count()
    test_users.delete()
    print(f"✅ Cleaned up {count} test users")

if __name__ == "__main__":
    print("🚀 USER CREATION FORMS CONSOLIDATION TEST")
    print("Testing both admin redirect and custom form functionality")
    print("=" * 80)

    try:
        test_admin_redirect()
        test_custom_form_functionality()
        test_pg_user_with_supervisor()
        test_form_validation()

        print(f"\n✨ All tests completed!")
        print("💡 Check results above for any issues")

    finally:
        cleanup_test_users()
