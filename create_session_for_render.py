"""
Session File Upload Script for Render Deployment
================================================
This script helps you authenticate Telegram locally and upload the session file
to Render as an environment variable (base64 encoded).

Run this locally BEFORE deploying to Render.
"""

import base64
import os
from telethon import TelegramClient

# Your credentials from .env
API_ID = os.getenv('TELEGRAM_API_ID', '31528324')
API_HASH = os.getenv('TELEGRAM_API_HASH', 'bb4e3ae5103442b0a30534d838e902da')
PHONE = os.getenv('TELEGRAM_PHONE', '+919585579490')
SESSION_NAME = 'discount_bot_session'


async def create_session():
    """Create and authenticate a Telegram session."""
    print("🔐 Creating Telegram Session for Render Deployment")
    print("=" * 60)
    print("\n📱 This will authenticate your Telegram account locally.")
    print("⚠️  You will need to enter the OTP code from Telegram.")
    print("💾 Then generate a session file you can upload to Render.")
    print("\n⭐ IMPORTANT: This only needs to be done ONCE!")
    print("   After this, no OTP will be needed on Render.\n")
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    print("\n🔌 Connecting to Telegram...")
    print("📱 Calling your phone number: {}\n".format(PHONE))
    
    # Start will automatically ask for OTP
    await client.start(phone=PHONE)
    
    me = await client.get_me()
    print(f"\n✅ Successfully authenticated as: {me.first_name}")
    print(f"📱 Phone: {me.phone}")
    
    await client.disconnect()
    
    # Read session file and encode it
    session_file = f"{SESSION_NAME}.session"
    if os.path.exists(session_file):
        with open(session_file, 'rb') as f:
            session_data = f.read()
        
        # Encode to base64
        encoded_session = base64.b64encode(session_data).decode('utf-8')
        
        print("\n" + "=" * 60)
        print("✅ Session Created Successfully!")
        print("=" * 60)
        print("\n📋 Copy this value and add it to Render environment variables:")
        print("\n⭐ IMPORTANT: Save this somewhere safe!")
        print("   You won't need to enter OTP again on Render.")
        print("\nVariable Name: TELEGRAM_SESSION")
        print("\nVariable Value:")
        print("-" * 60)
        print(encoded_session)
        print("-" * 60)
        
        print("\n📝 Instructions:")
        print("1. Go to Render Dashboard → Your Worker Service")
        print("2. Go to 'Environment' tab")
        print("3. Add new environment variable:")
        print("   Name: TELEGRAM_SESSION")
        print("   Value: (paste the encoded value above)")
        print("4. Save and redeploy")
        
        print("\n✅ Your bot will now work on Render without OTP!")
        print("⭐ The session is valid indefinitely - no re-authentication needed!")
    else:
        print(f"\n❌ Session file not found: {session_file}")


if __name__ == '__main__':
    import asyncio
    asyncio.run(create_session())
