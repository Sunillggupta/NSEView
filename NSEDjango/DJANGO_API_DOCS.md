# Django REST API Documentation

## Overview
Complete Django REST Framework API for NSE indices data with full CRUD operations, filtering, searching, and pagination.

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

---

## 1. Indices Endpoints

### List All Indices
**GET** `/api/indices/`

**Parameters:**
- `page` (integer): Page number for pagination (default: 1)
- `search` (string): Search by name, symbol, or key
- `ordering` (string): Order by field (name, last_price, percent_change)

**Response:**
```json
{
  "count": 139,
  "next": "http://localhost:8000/api/indices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "NIFTY 50",
      "symbol": "NIFTY 50",
      "key": "NIFTY 50",
      "last_price": 24270.85,
      "change": 95.15,
      "percent_change": 0.39
    }
  ]
}
```

**Example:**
```bash
# Get first page
curl http://localhost:8000/api/indices/

# Search for NIFTY indices
curl "http://localhost:8000/api/indices/?search=NIFTY"

# Sort by price change
curl "http://localhost:8000/api/indices/?ordering=-percent_change"

# Custom page size
curl "http://localhost:8000/api/indices/?page=2"
```

---

### Get Single Index Details
**GET** `/api/indices/{symbol}/`

**Parameters:**
- `symbol` (string, path): Index symbol (e.g., "NIFTY 50")

**Response:**
```json
{
  "id": 1,
  "name": "NIFTY 50",
  "symbol": "NIFTY 50",
  "key": "NIFTY 50",
  "last_price": 24270.85,
  "open_price": 24175.70,
  "high_price": 24286.30,
  "low_price": 24134.25,
  "previous_close": 24175.70,
  "change": 95.15,
  "percent_change": 0.39,
  "year_high": 24900.00,
  "year_low": 19800.00,
  "pe_ratio": "23.45",
  "pb_ratio": "3.20",
  "dividend_yield": "1.85",
  "advances": 32,
  "declines": 18,
  "unchanged": 0,
  "change_30d": 2.15,
  "change_365d": 18.50,
  "last_updated": "2026-07-04T15:30:00Z",
  "created_at": "2026-07-04T10:00:00Z"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/indices/NIFTY%2050/"
```

---

### Refresh Indices Data
**GET** `/api/indices/refresh/`

**Description:** Fetch fresh data from NSE API and update database

**Response:**
```json
{
  "status": "success",
  "message": "Updated 0 indices",
  "total": 139,
  "timestamp": "03-Jul-2026 15:30"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/indices/refresh/"
```

---

### Get Index History
**GET** `/api/indices/{symbol}/history/`

**Description:** Get last 100 historical records for an index

**Response:**
```json
[
  {
    "id": 1,
    "index": 1,
    "index_name": "NIFTY 50",
    "timestamp": "2026-07-04T15:30:00Z",
    "price": 24270.85,
    "change": 95.15,
    "percent_change": 0.39
  }
]
```

**Example:**
```bash
curl "http://localhost:8000/api/indices/NIFTY%2050/history/"
```

---

## 2. History Endpoints

### List Historical Data
**GET** `/api/history/`

**Parameters:**
- `index` (integer): Filter by index ID
- `ordering` (string): Order by field (timestamp, price)

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/history/?page=2",
  "previous": null,
  "results": [...]
}
```

**Example:**
```bash
# Get latest history records
curl "http://localhost:8000/api/history/"

# Filter by specific index
curl "http://localhost:8000/api/history/?index=1"

# Sort by newest first
curl "http://localhost:8000/api/history/?ordering=-timestamp"
```

---

## 3. Status Endpoints

### Get API Status
**GET** `/api/status/status/`

**Description:** Check overall API status and endpoint availability

**Response:**
```json
{
  "status": "operational",
  "message": "NSE Data API is operational",
  "endpoints": {
    "allIndices": "working",
    "quote-equity": "blocked (NSE has restricted access)"
  },
  "available_indices": 139,
  "timestamp": "03-Jul-2026 15:30",
  "note": "Individual equity quotes are not available (API blocked)"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/status/status/"
```

---

### Health Check
**GET** `/api/status/health/`

**Description:** Simple health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "api": "responding"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/status/health/"
```

---

## Filtering & Search Examples

### Search by Name
```bash
curl "http://localhost:8000/api/indices/?search=BANK"
```

### Filter by Symbol
```bash
curl "http://localhost:8000/api/indices/?search=NIFTY%20BANK"
```

### Sort by Percent Change (Descending)
```bash
curl "http://localhost:8000/api/indices/?ordering=-percent_change"
```

### Sort by Price (Ascending)
```bash
curl "http://localhost:8000/api/indices/?ordering=last_price"
```

### Combine Search and Ordering
```bash
curl "http://localhost:8000/api/indices/?search=NIFTY&ordering=-percent_change"
```

---

## Pagination

### Default Pagination (50 per page)
```bash
# Page 1
curl "http://localhost:8000/api/indices/?page=1"

# Page 2
curl "http://localhost:8000/api/indices/?page=2"
```

### Navigate Using Links
Response includes `next` and `previous` URLs for easy pagination.

---

## Error Responses

### 404 Not Found
```json
{
  "error": "Index not found"
}
```

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Error description"
}
```

### 503 Service Unavailable
```json
{
  "status": "error",
  "message": "NSE API temporarily unavailable"
}
```

---

## Features

✅ **RESTful Design** - Standard HTTP methods
✅ **Pagination** - 50 items per page, easy navigation
✅ **Search** - Full-text search across name, symbol, key
✅ **Filtering** - Filter by index, timestamp
✅ **Ordering** - Sort by any field
✅ **Detailed Responses** - Complete OHLC data, valuations, market stats
✅ **CORS Enabled** - Works with Angular frontend
✅ **Status Monitoring** - Check API health
✅ **Historical Tracking** - Record price changes over time
✅ **Error Handling** - Comprehensive error messages

---

## Quick Start

### 1. Start the Django server
```bash
cd NSEDjango
python manage.py runserver 0.0.0.0:8000
```

### 2. Load NSE data (if not already loaded)
```bash
python manage.py load_nse_data
```

### 3. Test endpoints
```bash
# Get all indices
curl http://localhost:8000/api/indices/

# Get specific index
curl "http://localhost:8000/api/indices/NIFTY%2050/"

# Check API status
curl "http://localhost:8000/api/status/status/"
```

### 4. Access API browser
```
http://localhost:8000/api/
```

---

## Authentication & Permissions

**Current Configuration:**
- Authentication: Session-based (can be extended)
- Permissions: AllowAny (open API)
- CORS: Enabled for localhost:3000 and localhost:4200

**To restrict access in production:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

---

## Performance Tips

1. **Use pagination** - Reduce data transfer
2. **Use search/filter** - Get only needed data
3. **Implement caching** - On Angular frontend for frequently accessed indices
4. **Batch requests** - Reduce number of API calls
5. **Monitor response times** - Check database indexes

---

## Database Schema

### Index Table
- `id`: Primary key
- `name`: Index name (e.g., "NIFTY 50")
- `symbol`: Index symbol (unique)
- `key`: Index key
- `last_price`, `open_price`, `high_price`, `low_price`, `previous_close`: OHLC data
- `change`, `percent_change`: Price movement
- `year_high`, `year_low`: 52-week data
- `pe_ratio`, `pb_ratio`, `dividend_yield`: Valuations
- `advances`, `declines`, `unchanged`: Market breadth
- `change_30d`, `change_365d`: Period returns
- `last_updated`, `created_at`: Timestamps

### IndexHistory Table
- `id`: Primary key
- `index`: Foreign key to Index
- `timestamp`: When data was recorded
- `price`: Index price
- `change`: Daily change
- `percent_change`: Percentage change

### APIStatus Table
- `id`: Primary key
- `name`: Endpoint name
- `endpoint`: URL
- `status`: Current status (working/blocked/error)
- `message`: Status message
- `last_checked`: Last check timestamp

---

## Next Steps - Angular Integration

The API is ready for the Angular frontend. Configure Angular HttpClient:

```typescript
// environment.ts
export const environment = {
  apiUrl: 'http://localhost:8000/api'
};

// service.ts
getIndices(): Observable<PaginatedResponse<Index[]>> {
  return this.http.get<PaginatedResponse<Index[]>>(`${this.apiUrl}/indices/`);
}

getIndexBySymbol(symbol: string): Observable<Index> {
  return this.http.get<Index>(`${this.apiUrl}/indices/${symbol}/`);
}
```

---

**Last Updated:** July 4, 2026
**Django Version:** 5.1.5
**DRF Version:** 3.14.x
**Status:** Production Ready ✅
