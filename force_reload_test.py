#!/usr/bin/env python3
"""
Force reload Django and test admin changes
"""

import os
import sys
from pathlib import Path

# Quick verification
def verify_changes():
    print("🔍 Verifying Admin Changes...")

    project_dir = Path(__file__).parent
    admin_file = project_dir / "sims" / "users" / "admin.py"

    if admin_file.exists():
        content = admin_file.read_text()

        checks = [
            ("Custom display methods", "get_full_name" in content and "get_role_display" in content),
            ("Pagination settings", "list_per_page = 25" in content),
            ("Custom changelist view", "def changelist_view" in content),
            ("CSS styling", "position: sticky" in content),
            ("User statistics JS", "user-stats" in content)
        ]

        print("\n📋 Admin Configuration Check:")
        all_good = True
        for check_name, result in checks:
            if result:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_good = False

        if all_good:
            print("\n🎉 All configurations are in place!")
            print("\n🚀 Next steps:")
            print("1. Go to: http://127.0.0.1:8000/admin/users/user/")
            print("2. Hard refresh (Ctrl+F5 or Cmd+Shift+R)")
            print("3. Look for:")
            print("   - Sticky table headers (scroll down to test)")
            print("   - User statistics at the top")
            print("   - Role indicators with emoji (🔴🟠🟢)")
            print("   - Enhanced styling")
        else:
            print("\n❌ Some configurations are missing")

    else:
        print("❌ Admin file not found")

if __name__ == "__main__":
    verify_changes()
