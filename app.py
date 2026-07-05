"""
NSE Data Web Application
Displays NSE indices and equity data on web pages using Flask
"""
from flask import Flask, render_template, jsonify, request
from nse_data import NSEDataFetcher
import json
from datetime import datetime

app = Flask(__name__)
fetcher = NSEDataFetcher()

@app.route('/')
def index():
    """Main page showing all indices"""
    try:
        all_data = fetcher.get_all_indices()
        indices = all_data.get('data', [])
        timestamp = all_data.get('timestamp', 'N/A')
        
        # Sort by index name for better organization
        indices.sort(key=lambda x: x.get('index', ''))
        
        return render_template('index.html', 
                             indices=indices, 
                             timestamp=timestamp,
                             total_count=len(indices))
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/index/<index_name>')
def index_detail(index_name):
    """Detailed view for a specific index"""
    try:
        index_data = fetcher.get_index_data(index_name)
        return render_template('index_detail.html', index=index_data)
    except Exception as e:
        return render_template('error.html', error=f"Index '{index_name}' not found"), 404

@app.route('/api/indices')
def api_indices():
    """API endpoint to get all indices as JSON"""
    try:
        all_data = fetcher.get_all_indices()
        return jsonify(all_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/index/<index_name>')
def api_index_detail(index_name):
    """API endpoint to get specific index data as JSON"""
    try:
        index_data = fetcher.get_index_data(index_name)
        return jsonify(index_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/equity/<symbol>')
def equity_quote(symbol):
    """Page for equity stock quote (shows limitation)"""
    try:
        quote = fetcher.get_equity_stock_quote(symbol)
        return render_template('equity_quote.html', 
                             symbol=symbol, 
                             quote=quote)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/about')
def about():
    """About page with documentation"""
    return render_template('about.html')

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'operational',
        'message': 'NSE Data API is operational',
        'working_endpoints': ['allIndices'],
        'blocked_endpoints': ['quote-equity (individual stocks)'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("NSE Data Web Application")
    print("=" * 60)
    print("Starting Flask server...")
    print("Navigate to: http://localhost:5000")
    print("API Endpoints:")
    print("  - GET /              : All indices")
    print("  - GET /index/<name>  : Index detail")
    print("  - GET /equity/<sym>  : Equity quote")
    print("  - GET /api/indices   : JSON API")
    print("  - GET /api/status    : Status")
    print("=" * 60)
    app.run(debug=True, host='localhost', port=5000)
