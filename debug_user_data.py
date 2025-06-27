#!/usr/bin/env python3
"""
Debug script to check actual user data and identify inaccuracies.
"""

import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def debug_user_data():
    """Check actual user data to identify inaccuracies."""
    print("🔍 DEBUGGING USER DATA")
    print("=" * 50)

    users = User.objects.all()
    print(f"Total users in database: {users.count()}")

    active_users = users.filter(is_active=True)
    inactive_users = users.filter(is_active=False)

    print(f"Active users (is_active=True): {active_users.count()}")
    print(f"Inactive users (is_active=False): {inactive_users.count()}")

    print("\n📊 USER STATUS BREAKDOWN:")
    for user in users[:10]:  # Show first 10 users
        status = "✅ Active" if user.is_active else "❌ Inactive"
        print(f"  {user.username}: {status} (is_active={user.is_active})")

    print("\n📊 ROLE BREAKDOWN:")
    roles = {}
    for user in users:
        role = user.role if hasattr(user, 'role') else 'Unknown'
        roles[role] = roles.get(role, 0) + 1

    for role, count in roles.items():
        print(f"  {role}: {count}")

    print("\n📊 STAFF STATUS:")
    staff_users = users.filter(is_staff=True)
    superusers = users.filter(is_superuser=True)
    print(f"Staff users: {staff_users.count()}")
    print(f"Superusers: {superusers.count()}")

if __name__ == '__main__':
    debug_user_data()
