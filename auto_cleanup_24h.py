"""
Automatic Cleanup Script - 24 Hour Policy
==========================================
Removes deals older than 24 hours from the database.

Run this script periodically (e.g., via cron or scheduled task):
- Every hour: */1 * * * * python auto_cleanup_24h.py
- Every 6 hours: 0 */6 * * * python auto_cleanup_24h.py

The script can be safely run multiple times - it only deletes old data.
"""

from supabase_database import init_database, cleanup_old_deals
from datetime import datetime

def main():
    print("=" * 60)
    print(f"🧹 Automatic Cleanup - 24 Hour Policy")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize database connection
    init_database()
    
    # Run cleanup
    deleted_count = cleanup_old_deals()
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup completed!")
    print(f"📊 Total deals deleted: {deleted_count}")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return deleted_count


if __name__ == "__main__":
    main()
