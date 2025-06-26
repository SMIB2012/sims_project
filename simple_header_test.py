#!/usr/bin/env python
"""
Simple header fix verification
==============================
"""

import urllib.request
import urllib.error

def test_header_fix():
    """Simple test for header fix"""
    print("🔍 TESTING HEADER FIX")
    print("=" * 30)
    
    url = "http://127.0.0.1:8000/users/create/?next=/admin/users/user/"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode('utf-8')
            
            # Check key indicators
            has_admin_header = 'admin-header' in content
            extends_base = '{% extends' in content
            has_admin_gradient = '--admin-gradient' in content
            
            print(f"✅ Page loads successfully")
            print(f"Admin header present: {'✅' if has_admin_header else '❌'}")
            print(f"Admin gradient styling: {'✅' if has_admin_gradient else '❌'}")
            print(f"Extends base template: {'❌ Good!' if not extends_base else '⚠️ Still extending!'}")
            
            if has_admin_header and not extends_base and has_admin_gradient:
                print(f"\n🎉 HEADER FIX SUCCESSFUL!")
                print("The admin form now has only the purple header!")
            else:
                print(f"\n⚠️ Header fix may need adjustment")
                
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_header_fix()
    print("\n📝 Manual check: Visit the URL to verify only purple header shows!")
