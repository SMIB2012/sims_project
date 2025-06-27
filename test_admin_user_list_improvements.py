#!/usr/bin/env python3
"""
Test script to verify the enhanced admin user list page improvements.
Tests the custom change_list template and UserAdmin enhancements.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.admin.sites import site
from sims.users.admin import UserAdmin

User = get_user_model()

def test_admin_user_list_improvements():
    """Test the enhanced admin user list functionality"""
    print("🔍 Testing Admin User List Improvements...")

    # 1. Test UserAdmin configuration
    print("\n1. Testing UserAdmin Configuration...")
    user_admin = UserAdmin(User, site)

    # Check list_display improvements
    expected_display = ('username', 'get_full_name', 'email', 'get_role_display',
                       'specialty', 'year', 'supervisor', 'get_status_display', 'date_joined')
    assert user_admin.list_display == expected_display, f"Expected {expected_display}, got {user_admin.list_display}"
    print("✅ list_display configuration correct")

    # Check pagination settings
    assert user_admin.list_per_page == 25, f"Expected 25, got {user_admin.list_per_page}"
    assert user_admin.list_max_show_all == 100, f"Expected 100, got {user_admin.list_max_show_all}"
    print("✅ Pagination settings correct")

    # 2. Test custom display methods
    print("\n2. Testing Custom Display Methods...")

    # Create test user
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        role='pg',
        is_active=True
    )

    # Test get_full_name method
    full_name = user_admin.get_full_name(test_user)
    assert full_name == "Test User", f"Expected 'Test User', got '{full_name}'"
    print("✅ get_full_name method working")

    # Test get_role_display method
    role_display = user_admin.get_role_display(test_user)
    assert "🟢" in role_display, f"Expected green circle for PG role, got '{role_display}'"
    print("✅ get_role_display method working")

    # Test get_status_display method
    status_display = user_admin.get_status_display(test_user)
    assert status_display == "✅ Active", f"Expected '✅ Active', got '{status_display}'"
    print("✅ get_status_display method working")

    # Test inactive user
    test_user.is_active = False
    test_user.save()
    status_display = user_admin.get_status_display(test_user)
    assert status_display == "❌ Inactive", f"Expected '❌ Inactive', got '{status_display}'"
    print("✅ Inactive status display working")

    # 3. Test template existence
    print("\n3. Testing Template Files...")

    template_path = project_dir / "templates" / "admin" / "users" / "user" / "change_list.html"
    assert template_path.exists(), f"Custom change_list template not found at {template_path}"
    print("✅ Custom change_list template exists")

    # Check template content
    template_content = template_path.read_text()
    assert "user-stats" in template_content, "Template missing user stats functionality"
    assert "sticky" in template_content, "Template missing sticky header functionality"
    assert "role-" in template_content, "Template missing role styling"
    print("✅ Template contains expected enhancements")

    # 4. Test with different roles
    print("\n4. Testing Different User Roles...")

    # Test admin role
    admin_user = User.objects.create_user(
        username='adminuser',
        email='admin@example.com',
        role='admin'
    )
    admin_display = user_admin.get_role_display(admin_user)
    assert "🔴" in admin_display, f"Expected red circle for admin role, got '{admin_display}'"
    print("✅ Admin role display working")

    # Test supervisor role
    supervisor_user = User.objects.create_user(
        username='supervisoruser',
        email='supervisor@example.com',
        role='supervisor'
    )
    supervisor_display = user_admin.get_role_display(supervisor_user)
    assert "🟠" in supervisor_display, f"Expected orange circle for supervisor role, got '{supervisor_display}'"
    print("✅ Supervisor role display working")

    # 5. Test method attributes
    print("\n5. Testing Method Attributes...")

    # Check method descriptions
    assert hasattr(user_admin.get_full_name, 'short_description'), "get_full_name missing short_description"
    assert user_admin.get_full_name.short_description == "Full Name", "get_full_name wrong description"

    assert hasattr(user_admin.get_role_display, 'short_description'), "get_role_display missing short_description"
    assert user_admin.get_role_display.short_description == "Role", "get_role_display wrong description"

    assert hasattr(user_admin.get_status_display, 'short_description'), "get_status_display missing short_description"
    assert user_admin.get_status_display.short_description == "Status", "get_status_display wrong description"
    assert user_admin.get_status_display.boolean == True, "get_status_display should be boolean field"

    print("✅ Method attributes correct")

    # Cleanup
    test_user.delete()
    admin_user.delete()
    supervisor_user.delete()

    print("\n🎉 All Admin User List Tests Passed!")
    return True

def test_template_responsiveness():
    """Test the responsive features in the template"""
    print("\n🔍 Testing Template Responsiveness...")

    template_path = project_dir / "templates" / "admin" / "users" / "user" / "change_list.html"
    template_content = template_path.read_text()

    # Check for responsive CSS
    responsive_features = [
        "@media (max-width: 1200px)",
        "@media (max-width: 992px)",
        "@media (max-width: 768px)",
        "display: none"
    ]

    for feature in responsive_features:
        assert feature in template_content, f"Missing responsive feature: {feature}"

    print("✅ Template has responsive design features")
    return True

def test_admin_permissions():
    """Test that admin permissions are preserved"""
    print("\n🔍 Testing Admin Permissions...")

    user_admin = UserAdmin(User, site)

    # Create test users
    superuser = User.objects.create_superuser(
        username='superuser',
        email='super@example.com',
        password='testpass'
    )

    admin_user = User.objects.create_user(
        username='adminuser',
        email='admin@example.com',
        role='admin'
    )

    regular_user = User.objects.create_user(
        username='regularuser',
        email='regular@example.com',
        role='pg'
    )

    # Create mock request objects
    class MockRequest:
        def __init__(self, user):
            self.user = user

    # Test superuser permissions
    superuser_request = MockRequest(superuser)
    assert user_admin.has_delete_permission(superuser_request) == True, "Superuser should have delete permission"

    # Test admin user permissions
    admin_request = MockRequest(admin_user)
    assert user_admin.has_delete_permission(admin_request) == True, "Admin should have delete permission"

    # Test regular user permissions
    regular_request = MockRequest(regular_user)
    assert user_admin.has_delete_permission(regular_request) == False, "Regular user should not have delete permission"

    print("✅ Admin permissions working correctly")

    # Cleanup
    superuser.delete()
    admin_user.delete()
    regular_user.delete()

    return True

def main():
    """Run all tests"""
    print("🚀 Starting Admin User List Enhancement Tests...")
    print("=" * 60)

    try:
        test_admin_user_list_improvements()
        test_template_responsiveness()
        test_admin_permissions()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Admin User List Enhancements are working correctly.")
        print("\nKey Improvements:")
        print("• ✅ Custom change_list template with compact design")
        print("• ✅ Sticky table headers for better scrolling")
        print("• ✅ Enhanced role displays with color coding")
        print("• ✅ User statistics dashboard")
        print("• ✅ Responsive design for mobile devices")
        print("• ✅ Improved status indicators")
        print("• ✅ Better pagination and search")
        print("• ✅ Preserved admin permissions")

        print("\nNext Steps:")
        print("1. Start the server: python manage.py runserver")
        print("2. Navigate to: http://127.0.0.1:8000/admin/users/user/")
        print("3. Login as admin and test the enhanced user list")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    main()
