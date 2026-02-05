"""
Deals E-Commerce Website
========================
A beautiful website to display all deals from the database.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from supabase_database import get_supabase_client, init_database
import os

app = Flask(__name__)
CORS(app)

# Initialize database
init_database()
supabase = get_supabase_client()


@app.route('/')
def index():
    """Main page."""
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
        limit = int(request.args.get('limit', 50))
        
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
            'count': len(response.data)
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
        response = supabase.table('active_deals').select('verified_discount, verified_price').execute()
        deals = response.data
        
        total_deals = len(deals)
        avg_discount = sum([d.get('verified_discount', 0) or 0 for d in deals]) / total_deals if total_deals > 0 else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_deals': total_deals,
                'avg_discount': round(avg_discount, 1),
                'categories': len(set([d.get('category') for d in deals if d.get('category')]))
            }
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n🚀 Starting Deals Website...")
    print(f"📱 Open: http://localhost:{port}")
    print("Press Ctrl+C to stop\n")
    app.run(debug=False, host='0.0.0.0', port=port)
