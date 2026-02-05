"""
Clear Database Script
====================
Deletes all records from deals and active_deals tables.
Use this to test with fresh data.
"""

from supabase_database import get_supabase_client, init_database

def clear_all_deals():
    """Delete all records from both tables."""
    
    # Initialize database connection
    init_database()
    supabase = get_supabase_client()
    
    if not supabase:
        print("❌ Failed to connect to database")
        return
    
    try:
        # Get counts before deletion
        deals_count = len(supabase.table('deals').select('id').execute().data)
        active_count = len(supabase.table('active_deals').select('id').execute().data)
        
        print(f"\n📊 Current records:")
        print(f"   deals: {deals_count}")
        print(f"   active_deals: {active_count}")
        
        # Confirm deletion
        confirm = input(f"\n⚠️  Delete ALL {deals_count + active_count} records? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("❌ Cancelled")
            return
        
        # Delete all records from active_deals
        print("\n🗑️  Deleting from active_deals...")
        result1 = supabase.table('active_deals').delete().neq('id', 0).execute()
        print(f"   ✅ Deleted from active_deals")
        
        # Delete all records from deals
        print("🗑️  Deleting from deals...")
        result2 = supabase.table('deals').delete().neq('id', 0).execute()
        print(f"   ✅ Deleted from deals")
        
        # Verify deletion
        deals_count_after = len(supabase.table('deals').select('id').execute().data)
        active_count_after = len(supabase.table('active_deals').select('id').execute().data)
        
        print(f"\n✅ Database cleared!")
        print(f"   deals: {deals_count_after}")
        print(f"   active_deals: {active_count_after}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    clear_all_deals()
