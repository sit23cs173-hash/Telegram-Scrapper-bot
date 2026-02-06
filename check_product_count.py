"""
Quick script to check how many products are in the database
"""
from supabase_database import get_supabase_client

# Initialize connection
client = get_supabase_client()

if client:
    # Count total deals
    result = client.table('deals').select('id', count='exact').execute()
    print(f"\n📊 Total products in 'deals' table: {result.count}")
    
    # Check active_deals view (if it exists)
    try:
        active_result = client.table('active_deals').select('id', count='exact').execute()
        print(f"📊 Total products in 'active_deals' view: {active_result.count}")
    except Exception as e:
        print(f"⚠️  'active_deals' view may not exist: {e}")
    
    # Show first few deals
    sample = client.table('deals').select('id, verified_title, store').limit(5).execute()
    print(f"\n📝 Sample of first 5 products:")
    for deal in sample.data:
        print(f"  - {deal.get('verified_title', 'N/A')} ({deal.get('store', 'N/A')})")
else:
    print("❌ Could not connect to database")
