"""
Fetch Historical Messages - Testing Tool
=========================================
Fetches the last N messages from channels and saves them to database.
"""

import asyncio
from datetime import datetime
from telethon import TelegramClient
from nlp_discount_parser import parse_discount_message
from supabase_database import save_to_database, init_database

# Telegram API credentials
API_ID = '31073628'
API_HASH = 'aa3d15671e6d93bf06ae350a77aa96bf'
SESSION_NAME = 'fetch_bot_session'  # Separate session file to avoid conflicts

# Channels and message count
TARGET_CHANNELS = [
    # Original channels
    'TrickXpert',
    
    # All offer/deal channels with public usernames
    'Alibaba_loots_dealsx',
    'bestlootdealsoffers2',
    'quality_loots',
    'icoolzTrickso_Official',
    'dealblastloot',
    'dealblast',
    'dealblastshop',
    'dealblastshopping',
    'dealblast_india_free_stuff',
    'DEALBLASTER8',
    'DealLoot99',
    'dealspointricks',
    'dealspoint',
    'dealsvelocity001',
    'DealTrigger',
    'realearnkaro100',
    'realearnkaro',
    'indiafreestuffin',
    'indiafreestffin',
    'KT_DEALS',
    'bestlootdeals07',
    'lootdealsapp1143',
    'lootdealsapp',
    'lootdealsapplication',
    'bestlootdeals',
    'Offerzone_Tricks_1',
    'Online_Loot_DealsX',
    'yashhotdealstore',
    'powerloot',
    'trickxperto',
    'tech24deals',
    'tech24deals9',
    'tech24deals_tech_24_deals',
    'Loot_DealsX',
    'Magixdeals_Tricks',
]

MESSAGES_PER_CHANNEL = 4


async def fetch_and_save_messages():
    """
    Fetch last N messages from each channel and save to database.
    """
    print("\n" + "=" * 80)
    print("📥 FETCHING HISTORICAL MESSAGES FOR TESTING")
    print("=" * 80 + "\n")
    
    # Initialize database
    print("🔌 Initializing Supabase...")
    init_database()
    print()
    
    # Initialize Telegram client
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"✅ Logged in as: {me.first_name}")
        print()
        
        total_processed = 0
        total_saved = 0
        
        # Fetch messages from each channel
        for channel in TARGET_CHANNELS:
            print(f"\n{'─' * 80}")
            print(f"📺 Channel: @{channel}")
            print(f"{'─' * 80}")
            
            try:
                # Get channel entity
                entity = await client.get_entity(channel)
                
                # Fetch last N messages
                messages = await client.get_messages(entity, limit=MESSAGES_PER_CHANNEL)
                
                print(f"📨 Found {len(messages)} messages")
                
                for i, msg in enumerate(messages, 1):
                    if not msg.text:
                        continue
                    
                    print(f"\n  Message {i}:")
                    print(f"  Text preview: {msg.text[:80]}...")
                    
                    # Parse with NLP
                    parsed = parse_discount_message(msg.text)
                    
                    # Add metadata
                    parsed['channel'] = getattr(entity, 'username', None) or getattr(entity, 'title', 'Unknown')
                    parsed['message_id'] = msg.id
                    parsed['message_date'] = msg.date.isoformat() if msg.date else None
                    
                    total_processed += 1
                    
                    # Validation checks
                    has_title = parsed.get('title') and len(parsed.get('title', '').strip()) > 0
                    has_link = parsed.get('link') and len(parsed.get('link', '').strip()) > 0
                    title_lower = parsed.get('title', '').strip().lower()
                    generic_titles = ['product', 'deal', 'offer', 'sale', 'item', 'clothing starts', 'products']
                    is_valid_title = title_lower not in generic_titles and len(title_lower) > 3
                    is_valid_link = has_link and not parsed['link'].startswith('https://t.me/')
                    has_valid_price = parsed.get('discount_price') and parsed['discount_price'] != '0'
                    
                    # Skip invalid deals
                    if not has_title or not has_link:
                        print(f"  ⏭️  Skipped (no title or link)")
                    elif not is_valid_title:
                        print(f"  ⏭️  Skipped (generic title)")
                    elif not is_valid_link:
                        print(f"  ⏭️  Skipped (telegram channel link, not product link)")
                    elif not has_valid_price:
                        print(f"  ⏭️  Skipped (invalid price: ₹{parsed.get('discount_price', 0)})")
                    else:
                        # Save to database
                        success = save_to_database(parsed)
                        if success:
                            total_saved += 1
                            print(f"  ✅ Saved: {parsed['title'][:50]}")
                            print(f"     Store: {parsed['store']} | Price: ₹{parsed['discount_price']}")
                        else:
                            print(f"  ⚠️  Failed to save")
                
            except Exception as e:
                print(f"  ❌ Error fetching from {channel}: {e}")
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"Channels processed : {len(TARGET_CHANNELS)}")
        print(f"Messages processed : {total_processed}")
        print(f"Messages saved     : {total_saved}")
        print("=" * 80)
        print("\n✅ Testing data loaded successfully!")
        print(f"\n🌐 View in Supabase: https://supabase.com/dashboard/project/sspufleiikzsazouzkot/editor")
        print()
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(fetch_and_save_messages())
