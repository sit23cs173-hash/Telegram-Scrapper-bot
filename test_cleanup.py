"""
Test and verify the cleanup_expired_deals() function.
Shows active vs expired deals before and after cleanup.
"""

from datetime import datetime, timezone
from supabase_database import init_database, cleanup_expired_deals
import supabase_database

def main():
    print("\n" + "=" * 80)
    print("TESTING CLEANUP FUNCTIONALITY - Active Deals Table")
    print("=" * 80)
    
    # Initialize
    print("\n🔌 Connecting to Supabase...")
    init_database()
    
    # Use the already initialized supabase client from the module
    supabase = supabase_database.supabase
    
    if not supabase:
        print("❌ Failed to initialize Supabase client")
        return
    
    # Get current time as timezone-aware datetime (UTC)
    now = datetime.now(timezone.utc)
    
    try:
        # Check active_deals table
        print("\n📊 Checking 'active_deals' table...")
        print("-" * 80)
        
        # Get all deals with their expiry dates
        all_deals = supabase.table('active_deals')\
            .select('id, title, offer_end_date')\
            .order('offer_end_date', desc=False)\
            .execute()
        
        total_count = len(all_deals.data)
        print(f"Total deals in active_deals: {total_count}")
        
        if total_count == 0:
            print("ℹ️  No deals found in active_deals table")
            return
        
        # Separate active and expired
        active_deals = []
        expired_deals = []
        no_expiry = []
        
        for deal in all_deals.data:
            if not deal.get('offer_end_date'):
                no_expiry.append(deal)
            else:
                try:
                    expiry_str = deal['offer_end_date']
                    
                    # Parse datetime - handle various formats
                    if 'T' in expiry_str:
                        # ISO format with potential timezone
                        expiry_str = expiry_str.replace('Z', '+00:00')
                        expiry_dt = datetime.fromisoformat(expiry_str)
                    else:
                        # Standard format without timezone
                        expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
                        # Make timezone-aware (assume UTC)
                        expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
                    
                    # Ensure both datetimes are timezone-aware for comparison
                    if expiry_dt.tzinfo is None:
                        expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
                    
                    if expiry_dt < now:
                        expired_deals.append(deal)
                    else:
                        active_deals.append(deal)
                        
                except Exception as e:
                    print(f"⚠️  Warning: Could not parse date for deal {deal['id']}: {e}")
                    no_expiry.append(deal)
        
        print(f"\n✅ Active deals (not expired): {len(active_deals)}")
        print(f"❌ Expired deals: {len(expired_deals)}")
        print(f"⚪ Deals with no expiry: {len(no_expiry)}")
        
        # Show sample expired deals
        if expired_deals:
            print(f"\n📋 Sample expired deals (showing first 5):")
            for deal in expired_deals[:5]:
                title = deal['title'][:50] + "..." if len(deal['title']) > 50 else deal['title']
                print(f"   • [{deal['id']}] {title}")
                print(f"     Expired: {deal['offer_end_date']}")
        
        # Show sample active deals
        if active_deals:
            print(f"\n📋 Sample active deals (showing first 5):")
            for deal in active_deals[:5]:
                title = deal['title'][:50] + "..." if len(deal['title']) > 50 else deal['title']
                print(f"   • [{deal['id']}] {title}")
                print(f"     Expires: {deal['offer_end_date']}")
        
        # Ask to run cleanup
        if expired_deals:
            print("\n" + "=" * 80)
            print(f"⚠️  Found {len(expired_deals)} expired deals ready for cleanup")
            print("=" * 80)
            
            response = input("\n🧹 Run cleanup now? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                print("\n🧹 Running cleanup...")
                deleted = cleanup_expired_deals()
                
                # Verify cleanup
                print("\n🔍 Verifying cleanup...")
                remaining = supabase.table('active_deals')\
                    .select('id', count='exact')\
                    .not_.is_('offer_end_date', 'null')\
                    .lt('offer_end_date', now.isoformat())\
                    .execute()
                
                remaining_count = remaining.count if hasattr(remaining, 'count') else len(remaining.data)
                
                if remaining_count == 0:
                    print("✅ All expired deals removed successfully!")
                else:
                    print(f"⚠️  {remaining_count} expired deals still remain")
                
                # Show final count
                final_count = supabase.table('active_deals').select('id', count='exact').execute()
                final_total = final_count.count if hasattr(final_count, 'count') else len(final_count.data)
                print(f"\n📊 Final count in active_deals: {final_total}")
            else:
                print("\n⏭️  Cleanup skipped")
        else:
            print("\n✅ No expired deals found - active_deals table is clean!")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETED")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
