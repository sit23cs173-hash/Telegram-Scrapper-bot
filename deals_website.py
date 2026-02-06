"""
Deals E-Commerce Website
========================
A beautiful website to display all deals from the database.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from supabase_database import get_supabase_client, init_database, cleanup_old_deals
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize database
init_database()
supabase = get_supabase_client()

# Track last cleanup time
last_cleanup = None


def auto_cleanup():
    """Run cleanup if it hasn't been run in the last hour."""
    global last_cleanup
    
    if last_cleanup is None or (datetime.now() - last_cleanup).seconds > 3600:
        print("🧹 Running automatic cleanup...")
        cleanup_old_deals()
        last_cleanup = datetime.now()


@app.route('/')
def index():
    """Main page."""
    # Run cleanup on page load (max once per hour)
    auto_cleanup()
    return render_template('index.html')


@app.route('/api/deals')
def get_deals():
    """API endpoint to fetch deals with filters."""
    try:
        # Get query parameters
        category = request.args.get('category', None)
        sort_by = request.args.get('sort', 'timestamp')
        order = request.args.get('order', 'desc')
        search = request.args.get('search', None)
        limit = int(request.args.get('limit', 10000))  # Increased default limit
        
        # Cap at reasonable maximum to prevent performance issues
        if limit > 10000:
            limit = 10000
        
        # Build query
        query = supabase.table('active_deals').select('*')
        
        # Apply filters
        if category and category != 'all':
            query = query.eq('category', category)
        
        if search:
            query = query.ilike('title', f'%{search}%')
        
        # Apply sorting
        if sort_by == 'discount':
            query = query.order('verified_discount', desc=(order == 'desc'))
        elif sort_by == 'price':
            query = query.order('verified_price', desc=(order == 'desc'))
        elif sort_by == 'rating':
            query = query.order('rating', desc=(order == 'desc'))
        else:  # timestamp
            query = query.order('timestamp', desc=(order == 'desc'))
        
        # Execute query
        query = query.limit(limit)
        response = query.execute()
        
        return jsonify({
            'success': True,
            'deals': response.data,
            'count': len(response.data),
            'total': len(response.data)  # Add total count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/categories')
def get_categories():
    """Get all available categories."""
    try:
        response = supabase.table('active_deals').select('category').execute()
        categories = list(set([deal['category'] for deal in response.data if deal.get('category')]))
        return jsonify({
            'success': True,
            'categories': sorted(categories)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """Get statistics."""
    try:
        # Get sample data for fast stats - limit to avoid timeout
        response = supabase.table('active_deals').select('verified_discount, verified_price, category').limit(1000).execute()
        deals = response.data
        
        total_deals = len(deals)
        avg_discount = sum([d.get('verified_discount', 0) or 0 for d in deals]) / total_deals if total_deals > 0 else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_deals': total_deals,  # This is a sample, full count would require separate query
                'avg_discount': round(avg_discount, 1),
                'categories': len(set([d.get('category') for d in deals if d.get('category')]))
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/cleanup')
def manual_cleanup():
    """Manual cleanup endpoint - removes deals older than 24 hours."""
    try:
        count = cleanup_old_deals()
        return jsonify({
            'success': True,
            'deleted': count,
            'message': f'Cleaned up {count} deals older than 24 hours'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


# Run cleanup on server startup
print("🧹 Running cleanup on server startup...")
cleanup_old_deals()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n🚀 Starting Deals Website...")
    print(f"📱 Open: http://localhost:{port}")
    print("Press Ctrl+C to stop\n")
    app.run(debug=False, host='0.0.0.0', port=port)
