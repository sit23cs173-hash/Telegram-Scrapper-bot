"""
Combined Web Server + Telegram Listener for Render Deployment
==============================================================
This runs the Telegram listener in a background thread while serving
a Flask web app for health checks (required for Render Web Service).
"""

from flask import Flask, jsonify
from flask_cors import CORS
import threading
import sys
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Store bot status
bot_status = {
    'running': False,
    'logged_in': False,
    'channels': 0,
    'messages_processed': 0,
    'last_error': None
}


@app.route('/')
def index():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Telegram Scraper Bot',
        'bot_status': bot_status
    })


@app.route('/health')
def health():
    """Detailed health check."""
    return jsonify(bot_status)


@app.route('/stats')
def stats():
    """Get bot statistics."""
    return jsonify({
        'status': 'ok',
        'bot_running': bot_status['running'],
        'logged_in': bot_status['logged_in'],
        'channels_monitoring': bot_status['channels'],
        'messages_processed': bot_status['messages_processed']
    })


def run_telegram_bot():
    """Run the Telegram listener in a background thread."""
    try:
        print("🤖 Starting Telegram listener in background thread...")
        bot_status['running'] = True
        
        # Import and run telegram listener
        from telegram_listener import main
        import asyncio
        
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the bot
        loop.run_until_complete(main())
        
    except Exception as e:
        print(f"❌ Telegram bot error: {e}")
        bot_status['last_error'] = str(e)
        bot_status['running'] = False


if __name__ == '__main__':
    # Start Telegram bot in background thread
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    print("🌐 Starting Flask web server for health checks...")
    
    # Start Flask web server (required for Render Web Service)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
