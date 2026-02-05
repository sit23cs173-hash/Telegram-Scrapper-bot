"""
Encode session file to base64 for Render deployment
"""
import base64
import os

SESSION_FILE = 'discount_bot_session.session'

if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, 'rb') as f:
        session_data = f.read()
    
    # Encode to base64
    encoded = base64.b64encode(session_data).decode('utf-8')
    
    print("\n" + "=" * 80)
    print("✅ SESSION FILE ENCODED FOR RENDER")
    print("=" * 80)
    print("\n📋 Add this to Render Environment Variables:")
    print("\n⭐ Variable Name: TELEGRAM_SESSION")
    print("\n📄 Variable Value (copy everything below):")
    print("-" * 80)
    print(encoded)
    print("-" * 80)
    
    print("\n📝 DEPLOYMENT INSTRUCTIONS:")
    print("=" * 80)
    print("\n1. Go to Render Dashboard: https://dashboard.render.com/")
    print("2. Select your 'telegram-scraper-bot' worker service")
    print("3. Go to 'Environment' tab")
    print("4. Click 'Add Environment Variable'")
    print("5. Add these variables:")
    print(f"\n   TELEGRAM_API_ID = {os.getenv('TELEGRAM_API_ID', 'YOUR_API_ID')}")
    print(f"   TELEGRAM_API_HASH = {os.getenv('TELEGRAM_API_HASH', 'YOUR_API_HASH')}")
    print(f"   TELEGRAM_SESSION = {encoded[:50]}...")
    print(f"   SUPABASE_URL = {os.getenv('SUPABASE_URL', 'YOUR_SUPABASE_URL')}")
    print(f"   SUPABASE_KEY = {os.getenv('SUPABASE_KEY', 'YOUR_SUPABASE_KEY')[:50]}...")
    print("\n6. Click 'Save Changes'")
    print("7. Render will automatically redeploy")
    print("\n✅ Bot will start WITHOUT asking for OTP!")
    print("=" * 80 + "\n")
    
    # Save to file for reference
    with open('TELEGRAM_SESSION_ENCODED.txt', 'w') as f:
        f.write(encoded)
    print("💾 Also saved to: TELEGRAM_SESSION_ENCODED.txt\n")
    
else:
    print(f"\n❌ Session file not found: {SESSION_FILE}")
    print("\n📝 To create session file:")
    print("   python create_session_for_render.py\n")
