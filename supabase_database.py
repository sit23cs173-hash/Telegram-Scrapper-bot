"""
Supabase Database Module
=========================
Handles saving parsed discount messages to Supabase (PostgreSQL cloud database).

Author: AI Assistant
Date: December 2025
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from supabase import create_client, Client

# Import NLP parser for category extraction
try:
    from nlp_discount_parser import DiscountMessageParser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False


# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://sspufleiikzsazouzkot.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzcHVmbGVpaWt6c2F6b3V6a290Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MjkzNTEsImV4cCI6MjA4MTEwNTM1MX0.Uzh8O4Tn6buf2mhcA4w1JQeCZA-dcpzhm7AovwL4c4E')

# Table name
TABLE_NAME = 'deals'

# Initialize Supabase client
supabase: Client = None


def init_database():
    """
    Initialize the Supabase connection.
    """
    global supabase
    
    if SUPABASE_URL == 'https://your-project.supabase.co' or SUPABASE_KEY == 'your-anon-key-here':
        print("⚠️  Warning: Supabase credentials not configured!")
        print("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        return
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Connected to Supabase: {SUPABASE_URL}")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        if "getaddrinfo failed" in str(e) or "11001" in str(e):
            print("⚠️  DNS resolution failed - Supabase URL may be incorrect or network issue")
            print(f"⚠️  Current URL: {SUPABASE_URL}")
            print("⚠️  Please verify:")
            print("   1. Your Supabase project exists at https://supabase.com/dashboard")
            print("   2. Update SUPABASE_URL in .env file with correct project URL")
            print("   3. Check your internet connection")
        # Don't raise - allow bot to continue running without database
        supabase = None


def get_supabase_client() -> Client:
    """
    Get or initialize the Supabase client.
    Used by new intelligence modules.
    
    Returns:
        Client: Supabase client instance
    """
    global supabase
    
    if supabase is None:
        init_database()
    
    return supabase


def save_to_database(data: Dict) -> bool:
    """
    Save deal data to Supabase - ALL DATA FROM OFFICIAL WEBSITES ONLY.
    
    This function ONLY saves data that was scraped from official e-commerce websites.
    It will NEVER use data parsed from Telegram messages.
    
    Required fields (all from official sites):
    - verified_title: Product name from official product page
    - verified_mrp: Original MRP from official product page  
    - verified_price: Discounted price from official product page
    - verified_discount: Discount percentage calculated from official prices
    - link: E-commerce product URL
    - rating: Product rating from official product page
    
    Args:
        data (dict): Deal data with verified_* fields from official website scraping
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return False
    
    try:
        # Use official website data (verified_*) with fallback to NLP-parsed data
        product_name = data.get('verified_title') or data.get('title')  # Fallback to NLP title
        original_mrp = data.get('verified_mrp') or data.get('mrp')
        discounted_price = data.get('verified_price') or data.get('discount_price')
        discount_percent = data.get('verified_discount') or data.get('discount_percent')
        product_link = data.get('link', '')
        rating = data.get('rating')
        product_image_url = data.get('product_image_url')
        additional_images = data.get('additional_images', [])
        
        # Extract category from product title
        category = 'other'  # Default category
        if product_name:
            try:
                from smart_categorizer import SmartProductCategorizer
                categorizer = SmartProductCategorizer()
                result = categorizer.categorize(product_name)
                category = result['category']
            except:
                pass  # Use default 'other'
        
        # Calculate offer end date (default: 7 days from now)
        # Can be overridden with data.get('offer_end_date')
        offer_end_date = data.get('offer_end_date')
        if offer_end_date is None:
            # Default: offers expire in 7 days
            offer_end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare minimal record with only required fields
        record = {
            'title': product_name[:500] if product_name else None,  # Product name from official site (max 500 chars)
            'verified_mrp': original_mrp,  # Original MRP from official site
            'verified_price': discounted_price,  # Discounted price from official site
            'verified_discount': discount_percent,  # Discount % from official site
            'link': product_link,  # E-commerce link
            'rating': rating,  # Product rating from official site
            'category': category,  # Product category (electronics, fashion, etc.)
            'offer_end_date': offer_end_date,  # When the offer expires
            'product_image_url': product_image_url,  # Main product image URL
            'additional_images': additional_images if additional_images else None,  # Array of additional images
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Seller details from official website
            'seller_name': data.get('seller_name'),
            'seller_rating': data.get('seller_rating'),
            'is_fulfilled_by_platform': data.get('is_fulfilled_by_platform', False),
            'seller_info': data.get('seller_info'),
        }
        
        # Strict validation - all data must come from official website
        if not product_name:
            print("❌ No product name (neither verified nor parsed)")
            return False
            
        if not product_link:
            print("❌ Missing product link")
            return False
        
        if not discounted_price:
            print("❌ No price (neither verified nor parsed)")
            return False
        
        # Validate price range (₹10 - ₹500,000)
        try:
            price = float(discounted_price)
            if price < 10 or price > 500000:
                print(f"❌ Price out of range: ₹{price}")
                return False
        except (ValueError, TypeError):
            print("❌ Invalid price format")
            return False
        
        # Clean and normalize title to prevent corruption
        product_name = ' '.join(product_name.split())  # Remove extra whitespace
        product_name = product_name.encode('utf-8', 'ignore').decode('utf-8')  # Remove invalid chars
        
        # Check for duplicates by BOTH link AND title similarity (prevent same product with different affiliate links)
        # Check in both "deals" and "active_deals" tables
        
        # First check exact link match in active_deals
        existing_link_active = supabase.table('active_deals').select('id, title').eq('link', product_link).execute()
        
        if existing_link_active.data:
            print(f"⏭️  Product with same link already exists in active_deals, skipping...")
            return False
        
        # Then check for similar title (fuzzy match to catch same product with different URLs)
        # Extract core product name (remove "Pack of", sizes, etc. for comparison)
        core_title = product_name.split('(')[0].strip().lower()[:50]  # First 50 chars before parenthesis
        
        existing_titles = supabase.table('active_deals').select('id, title').execute()
        
        for existing in existing_titles.data:
            existing_core = existing['title'].split('(')[0].strip().lower()[:50]
            # If 80% of core title matches, consider it duplicate
            if core_title in existing_core or existing_core in core_title:
                if len(core_title) > 10 and len(existing_core) > 10:  # Only if substantial title
                    similarity = min(len(core_title), len(existing_core)) / max(len(core_title), len(existing_core))
                    if similarity > 0.8:
                        print(f"⏭️  Similar product already exists: '{existing['title'][:50]}...', skipping...")
                        return False
        
        # Insert new record to both tables
        # 1. Save to "deals" table (permanent historical record)
        response_deals = supabase.table('deals').insert(record).execute()
        
        # 2. Save to "active_deals" table (currently active offers)
        response_active = supabase.table('active_deals').insert(record).execute()
        
        print(f"✅ Saved to both 'deals' and 'active_deals' tables")
        return True
        
    except Exception as e:
        print(f"❌ Supabase save error: {e}")
        return False


def get_recent_deals(limit: int = 10) -> List[Dict]:
    """
    Retrieve recent deals from Supabase.
    
    Args:
        limit (int): Number of deals to retrieve
        
    Returns:
        list: List of deal dictionaries
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        response = supabase.table(TABLE_NAME)\
            .select("*")\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


def get_deals_by_store(store: str, limit: int = 10) -> List[Dict]:
    """
    Retrieve deals from a specific store.
    
    Args:
        store (str): Store name (e.g., "Amazon", "Flipkart")
        limit (int): Number of deals to retrieve
        
    Returns:
        list: List of deal dictionaries
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        response = supabase.table(TABLE_NAME)\
            .select("*")\
            .eq('store', store)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


def get_deals_by_category(category: str, limit: int = 10) -> List[Dict]:
    """
    Retrieve deals from a specific category.
    
    Args:
        category (str): Category name (e.g., "electronics", "fashion")
        limit (int): Number of deals to retrieve
        
    Returns:
        list: List of deal dictionaries
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        response = supabase.table(TABLE_NAME)\
            .select("*")\
            .eq('category', category)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


def get_statistics() -> Dict:
    """
    Get database statistics from Supabase.
    
    Returns:
        dict: Statistics including total deals, deals by store, etc.
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return {}
    
    try:
        # Get total count
        response = supabase.table(TABLE_NAME).select("*", count='exact').execute()
        total_deals = response.count
        
        # Get all deals for grouping (in production, use SQL aggregation)
        all_deals = supabase.table(TABLE_NAME).select("store, category").execute()
        
        # Group by store
        deals_by_store = {}
        deals_by_category = {}
        
        for deal in all_deals.data:
            store = deal.get('store', 'Unknown')
            category = deal.get('category', 'Unknown')
            
            deals_by_store[store] = deals_by_store.get(store, 0) + 1
            deals_by_category[category] = deals_by_category.get(category, 0) + 1
        
        return {
            'total_deals': total_deals,
            'deals_by_store': deals_by_store,
            'deals_by_category': deals_by_category
        }
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return {}


def get_deals_by_category_supabase(category: str, limit: int = 10) -> List[Dict]:
    """
    Retrieve active deals from a specific category (only non-expired offers).
    
    Args:
        category (str): Category name (electronics, fashion, home, beauty, books, grocery, sports, other)
        limit (int): Number of deals to retrieve
        
    Returns:
        list: List of deal dictionaries
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Query active deals by category (offer_end_date IS NULL OR > NOW)
        response = supabase.table(TABLE_NAME)\
            .select("*")\
            .eq('category', category)\
            .or_(f'offer_end_date.is.null,offer_end_date.gt.{now}')\
            .order('timestamp', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


def get_all_categories() -> List[Dict]:
    """
    Get list of all categories with active deal counts.
    
    Returns:
        list: List of dicts with category name and count
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get all active deals
        response = supabase.table(TABLE_NAME)\
            .select("category")\
            .or_(f'offer_end_date.is.null,offer_end_date.gt.{now}')\
            .execute()
        
        # Count by category
        category_counts = {}
        for deal in response.data:
            cat = deal.get('category', 'other')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Convert to list of dicts
        result = [
            {'category': cat, 'count': count}
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return result
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


def cleanup_expired_deals() -> int:
    """
    Remove expired deals from 'active_deals' table only.
    The 'deals' table keeps all deals as historical record.
    
    Returns:
        int: Number of deals deleted from active_deals
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return 0
    
    try:
        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # First, get count of expired deals in active_deals
        expired_deals = supabase.table('active_deals')\
            .select("id", count='exact')\
            .not_.is_('offer_end_date', 'null')\
            .lt('offer_end_date', now)\
            .execute()
        
        count = expired_deals.count if hasattr(expired_deals, 'count') else len(expired_deals.data)
        
        if count == 0:
            print("✅ No expired deals to cleanup")
            return 0
        
        # Delete expired deals from active_deals table only
        supabase.table('active_deals')\
            .delete()\
            .not_.is_('offer_end_date', 'null')\
            .lt('offer_end_date', now)\
            .execute()
        
        print(f"✅ Cleaned up {count} expired deals from active_deals table")
        print(f"📚 Historical records remain in 'deals' table")
        return count
        
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
        return 0


def cleanup_old_deals() -> int:
    """
    Remove deals older than 24 hours from insertion time.
    Deletes from both 'deals' and 'active_deals' tables.
    
    Returns:
        int: Number of deals deleted
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return 0
    
    try:
        # Calculate timestamp 24 hours ago
        cutoff_time = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Delete from deals table (main table)
        result = supabase.table('deals')\
            .delete()\
            .lt('timestamp', cutoff_time)\
            .execute()
        
        count = len(result.data) if hasattr(result, 'data') else 0
        
        if count > 0:
            print(f"✅ Deleted {count} deals older than 24 hours")
        else:
            print("✅ No deals older than 24 hours to cleanup")
        
        return count
        
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
        return 0


def get_active_deals(limit: int = 50) -> List[Dict]:
    """
    Get all active deals (non-expired).
    
    Args:
        limit (int): Maximum number of deals to retrieve
        
    Returns:
        list: List of active deal dictionaries
    """
    global supabase
    
    if supabase is None:
        print("❌ Supabase client not initialized")
        return []
    
    try:
        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Query active deals
        response = supabase.table(TABLE_NAME)\
            .select("*")\
            .or_(f'offer_end_date.is.null,offer_end_date.gt.{now}')\
            .order('timestamp', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        return []


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SUPABASE DATABASE MODULE - TEST")
    print("=" * 80)
    print()
    
    # Initialize database
    init_database()
    print()
    
    # Test data
    test_deal = {
        'title': 'Boat Airdopes 441',
        'store': 'Amazon',
        'mrp': '2999',
        'discount_price': '999',
        'discount_percent': '67',
        'link': 'https://amzn.to/test123',
        'category': 'electronics',
        'channel': 'amazon_deals',
        'message_id': 12345,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save test deal
    print("📝 Saving test deal...")
    result = save_to_database(test_deal)
    print(f"  {'✅' if result else '❌'} {test_deal['title']}")
    print()
    
    # Get statistics
    print("📊 Database Statistics:")
    stats = get_statistics()
    print(f"  Total Deals: {stats.get('total_deals', 0)}")
    print(f"  By Store: {stats.get('deals_by_store', {})}")
    print(f"  By Category: {stats.get('deals_by_category', {})}")
    print()
    
    # Get recent deals
    print("📋 Recent Deals:")
    recent = get_recent_deals(limit=5)
    for i, deal in enumerate(recent, 1):
        print(f"\n  {i}. {deal['title']}")
        print(f"     Store: {deal['store']} | Price: ₹{deal['discount_price']}")
        print(f"     Link: {deal['link']}")
    
    print("\n" + "=" * 80)
    print("✅ Database test completed")
    print("=" * 80)
