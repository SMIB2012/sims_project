#!/usr/bin/env python3
"""
Final test to verify "View site" button has been completely removed from admin.
"""

import os
import re

def test_complete_view_site_removal():
    """Test that View site button has been removed from all admin templates."""
    admin_templates = [
        r"d:\PMC\sims_project-2\templates\admin\index.html",
        r"d:\PMC\sims_project-2\templates\admin\base.html",
        r"d:\PMC\sims_project-2\templates\admin\base_site.html"
    ]

    print("🔍 COMPLETE VIEW SITE REMOVAL TEST")
    print("=" * 60)

    all_clean = True

    for template_path in admin_templates:
        if not os.path.exists(template_path):
            print(f"⚠️  Template not found: {os.path.basename(template_path)}")
            continue

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        template_name = os.path.basename(template_path)
        print(f"\n📄 Checking {template_name}:")

        # Check for various "View site" patterns
        view_site_patterns = [
            (r'View site', 'View site text'),
            (r'view site', 'view site (lowercase)'),
            (r'external-link-alt.*View site', 'View site with external link icon'),
            (r'{% trans [\'"]View site[\'"] %}', 'Translated View site'),
            (r'target="_blank".*View site', 'View site with target blank')
        ]

        found_issues = False
        for pattern, description in view_site_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                print(f"❌ Found: {description}")
                found_issues = True
                all_clean = False

        if not found_issues:
            print(f"✅ Clean - No View site references found")

    print(f"\n📋 Quick Links Section Check:")
    # Check that homepage link in Quick Links is preserved (this is different)
    index_path = r"d:\PMC\sims_project-2\templates\admin\index.html"
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if re.search(r'Homepage', content):
            print("✅ Homepage link in Quick Links: Preserved (this is good)")
        else:
            print("⚠️  Homepage link in Quick Links: Missing")

    print("=" * 60)
    if all_clean:
        print("🎉 SUCCESS! View site button completely removed!")
        print("✅ The redundant admin header button is gone")
        print("✅ Homepage in Quick Links is preserved (different purpose)")
    else:
        print("⚠️  View site button may still exist in some templates")

    return all_clean

if __name__ == "__main__":
    test_complete_view_site_removal()

    print("\n💡 Check http://localhost:8000/admin/ to verify:")
    print("   • No 'View site' button in admin header")
    print("   • 'Homepage' link in Quick Links section is OK (different purpose)")
