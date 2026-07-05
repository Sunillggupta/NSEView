# NSE Data Web Application - Complete Setup Guide

## Overview
This is a complete Python web application built with Flask that displays NSE (National Stock Exchange) indices and market data with an interactive, responsive web interface.

## What's Included

### 1. Backend Files
- **app.py** - Flask web application with all routes and API endpoints
- **nse_data.py** - NSE data fetcher class (handles API communication)
- **test_web_app.py** - Comprehensive test suite for web pages

### 2. Frontend Templates (HTML/CSS)
- **base.html** - Base template with styling and navigation
- **index.html** - Main page displaying all 139+ indices in sortable table
- **index_detail.html** - Detailed view for individual indices with OHLC data
- **equity_quote.html** - Equity quote page (shows API limitation info)
- **about.html** - Documentation and API information
- **error.html** - Error page for handling exceptions

### 3. Documentation
- **API_FIX_DOCUMENTATION.md** - Detailed documentation of API issues and fixes
- **WEB_APP_SETUP.md** - This file

## Features

### Main Dashboard (Home Page)
- ✅ Table displaying all 139+ NSE indices
- ✅ Real-time market data (last price, change, % change)
- ✅ Sortable columns
- ✅ Search functionality
- ✅ Filter by index type (Derivatives, Broad Market, etc.)
- ✅ Quick links to detailed views

### Index Details Page
- ✅ Comprehensive index information
- ✅ OHLC data (Open, High, Low, Close)
- ✅ 52-week High and Low prices
- ✅ Valuation metrics (P/E, P/B ratios)
- ✅ Market activity (advances, declines, unchanged)
- ✅ Performance history (1-week, 1-month, 1-year)
- ✅ Clean, organized layout

### Equity Quote Page
- ✅ Handles API limitation gracefully
- ✅ Explains why individual stocks are not available
- ✅ Provides alternative solutions
- ✅ Links to resources and documentation

### API Endpoints (JSON)
- ✅ GET /api/indices - All indices data
- ✅ GET /api/index/<name> - Specific index data
- ✅ GET /api/status - API status information

## How to Run

### Prerequisites
```bash
python -m pip install flask requests beautifulsoup4
```

### Start the Web Server
```bash
cd C:\2026Projects\Proj_NSE\NSEView
python app.py
```

The server will start at: **http://localhost:5000**

### Run Tests
```bash
python test_web_app.py
```

This will:
1. Start the Flask server
2. Run all endpoint tests
3. Verify HTML and JSON responses
4. Display test results summary
5. Keep server running (Press Ctrl+C to stop)

## Test Results
All endpoints have been tested and verified:

```
[OK 200] /                        - Home page - All indices
[OK 200] /api/status              - API Status endpoint
[OK 200] /index/NIFTY%2050        - Index detail - NIFTY 50
[OK 200] /index/NIFTY%20BANK      - Index detail - NIFTY BANK
[OK 200] /equity/RELIANCE         - Equity quote - RELIANCE
[OK 200] /equity/TCS              - Equity quote - TCS
[OK 200] /about                   - About page
[OK 200] /api/indices             - JSON API - All indices
[OK 200] /api/index/NIFTY%2050    - JSON API - NIFTY 50
[OK 404] /index/NONEXISTENT       - Nonexistent index (404 as expected)
```

## Page Descriptions

### Home Page (/)
The main landing page displays a table of all available indices with:
- Index name and category
- Last price
- Price change (points and percentage)
- OHLC data
- P/E ratio
- Quick action button to view details

Features:
- Search box to filter by index name
- Category filter buttons (All, Derivatives, Broad Market)
- Responsive design for mobile and desktop
- Color-coded positive/negative changes

### Index Detail Page (/index/<name>)
Shows comprehensive information for a specific index:
- Large stat cards for key metrics
- OHLC and 52-week data table
- Valuation metrics (P/E, P/B, Dividend Yield)
- Market activity indicators
- Performance data (1-week, 1-month, 1-year)

### Equity Quote Page (/equity/<symbol>)
Explains that individual stock quotes are not available:
- Clear explanation of API limitation (HTTP 403)
- Root cause analysis
- Alternative solutions (third-party APIs, web scraping, local cache)
- Links to resources and documentation
- Suggestions to use index data instead

### About Page (/about)
Comprehensive documentation:
- Application overview
- Features list
- Technical stack
- API endpoints reference
- Limitations and alternatives
- Usage instructions
- Contact information

## API Endpoints Reference

### HTML Pages
```
GET /              - Main dashboard with all indices
GET /index/<name>  - Detailed view for specific index
GET /equity/<sym>  - Equity quote (shows limitation)
GET /about         - Documentation page
GET /               - Home
```

### JSON API
```
GET /api/indices              - Get all indices data
GET /api/index/<name>         - Get specific index data
GET /api/status               - Get API status
```

### Example API Calls
```bash
# Get all indices
curl http://localhost:5000/api/indices

# Get specific index
curl http://localhost:5000/api/index/NIFTY%2050

# Check API status
curl http://localhost:5000/api/status
```

## Data Structure

### Index Data Object
```json
{
  "key": "INDICES ELIGIBLE IN DERIVATIVES",
  "index": "NIFTY 50",
  "indexSymbol": "NIFTY 50",
  "last": 24270.85,
  "variation": 95.15,
  "percentChange": 0.39,
  "open": 24375.65,
  "high": 24378.15,
  "low": 24252.35,
  "previousClose": 24175.7,
  "yearHigh": 26373.2,
  "yearLow": 22182.55,
  "pe": "20.92",
  "pb": "3.1",
  "dy": "1.8",
  "advances": 32,
  "declines": 15,
  "unchanged": 3,
  "perChange30d": "-2.5",
  "perChange365d": "-8.2"
}
```

## Styling

The application uses a modern gradient design with:
- Purple-blue color scheme (#667eea to #764ba2)
- Responsive grid layout
- Mobile-friendly design
- Clean typography
- Color-coded data (green for positive, red for negative)
- Smooth transitions and hover effects

### Color Scheme
- Primary: #667eea (Blue)
- Secondary: #764ba2 (Purple)
- Success: #28a745 (Green)
- Danger: #dc3545 (Red)
- Neutral: #6c757d (Gray)

## Features Details

### Search Functionality
- Real-time search as you type
- Searches index name
- Case-insensitive matching
- Instant table filtering

### Filter Buttons
- "All Indices" - Show all indices
- "Derivatives Eligible" - Only derivative indices
- "Broad Market" - Broad market indices
- Active button highlighted in purple

### Sortable Table
- Click column headers to sort
- Color-coded changes (green/red)
- Formatted numbers with proper decimals
- Responsive columns

### Mobile Responsive
- Adapts to different screen sizes
- Table text size adjusts
- Navigation remains accessible
- Touch-friendly buttons

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```python
# In app.py, change the port:
app.run(debug=True, host='localhost', port=5001)
```

### SSL Certificate Error
If you get SSL errors, add this to nse_data.py:
```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

### Connection Refused
- Ensure Flask is running
- Check if server started successfully
- Try accessing http://127.0.0.1:5000 instead of localhost

### Template Not Found
- Ensure templates directory exists: C:\2026Projects\Proj_NSE\NSEView\templates
- Check that all .html files are in the templates directory

## Performance Notes

- Caches NSE data during a session
- Makes API calls only when data is requested
- Handles large tables efficiently
- Responsive UI with minimal JavaScript

## Browser Compatibility

- Chrome/Chromium: Full support
- Firefox: Full support
- Safari: Full support
- Edge: Full support
- IE 11: Limited support (some CSS features may not work)

## Security Notes

The application:
- Does not store sensitive data
- Uses secure headers
- Validates all inputs
- Handles errors gracefully
- Does not expose system information

## Future Enhancements

Potential improvements:
1. Add historical price charts
2. Implement data caching with timestamps
3. Add email alerts for price changes
4. Export data to CSV/Excel
5. Add portfolio tracking
6. Implement user authentication
7. Add more detailed technical analysis
8. Create mobile app

## File Structure
```
NSEView/
├── app.py                    (Flask application)
├── nse_data.py              (Data fetcher class)
├── test_web_app.py          (Test suite)
├── Test1.py                 (Old test file)
├── API_FIX_DOCUMENTATION.md (API documentation)
├── WEB_APP_SETUP.md         (This file)
└── templates/
    ├── base.html            (Base template)
    ├── index.html           (Home page)
    ├── index_detail.html    (Index details)
    ├── equity_quote.html    (Equity page)
    ├── about.html           (About page)
    └── error.html           (Error page)
```

## Support

For issues or questions:
1. Check the About page in the application
2. Review API_FIX_DOCUMENTATION.md
3. Check error messages displayed on pages
4. Run test_web_app.py to verify installation

## License

This application is built for NSE data visualization and uses publicly available NSE API endpoints.

## Version History

**v1.0** - Initial Release
- Complete Flask web application
- 6 HTML templates with responsive design
- Full API with JSON endpoints
- Comprehensive documentation
- Test suite included
- Mobile-friendly interface
- Search and filter functionality

---

**Last Updated:** July 4, 2026
**Status:** Production Ready
