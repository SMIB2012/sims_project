#!/usr/bin/env python3
"""
Test script to verify "View Site" button has been removed from admin dashboard.
"""

import os
import re

def test_view_site_button_removal():
    """Test that the View Site button has been removed."""
    template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"

    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("🔍 Testing View Site Button Removal...")
    print("=" * 50)

    # Check for "View Site" text
    view_site_patterns = [
        r'View Site',
        r'view site',
        r'VIEW SITE'
    ]

    found_view_site = False
    for pattern in view_site_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"❌ Found '{pattern}' in template")
            found_view_site = True

    if not found_view_site:
        print("✅ No 'View Site' text found in template")

    # Check for external link icon that was used with View Site
    external_link_pattern = r'<i class="fas fa-external-link-alt[^"]*"[^>]*></i>\s*View Site'
    if re.search(external_link_pattern, content, re.MULTILINE | re.DOTALL):
        print("❌ View Site button with external link icon still found")
        found_view_site = True
    else:
        print("✅ View Site button with external link icon not found")

    # Check for home URL reference in context of View Site
    home_url_view_site_pattern = r'{%\s*url\s+[\'"]home[\'"]\s*as\s+home_url\s*%}.*?View Site'
    if re.search(home_url_view_site_pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
        print("❌ Home URL reference for View Site still found")
        found_view_site = True
    else:
        print("✅ Home URL reference for View Site not found")

    # Check that other buttons are still present
    other_buttons = [
        ('Admin Analytics', r'Admin Analytics'),
        ('Users link', r'All Users'),
        ('Homepage link', r'Homepage')
    ]

    print(f"\n📋 Other Navigation Elements Check:")
    for button_name, pattern in other_buttons:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ {button_name}: Still present")
        else:
            print(f"⚠️  {button_name}: Not found")

    print("=" * 50)
    if not found_view_site:
        print("🎉 View Site button successfully removed!")
        print("✅ The redundant button that redirected to itself is gone")
    else:
        print("⚠️  View Site button may still be present")

    return not found_view_site

if __name__ == "__main__":
    print("🚀 VIEW SITE BUTTON REMOVAL TEST")
    print("Testing removal of redundant View Site button")
    print("=" * 60)

    test_view_site_button_removal()

    print("\n✨ Test completed!")
    print("💡 Check the admin dashboard: http://localhost:8000/admin/")
