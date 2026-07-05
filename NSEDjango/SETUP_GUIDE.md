# Django REST API Setup Guide

## Project Structure

```
NSEDjango/
├── nse_project/              # Main Django project
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Project URL routing
│   ├── asgi.py
│   └── wsgi.py
├── api/                       # Django app
│   ├── migrations/            # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── load_nse_data.py
│   ├── models.py             # Database models (Index, IndexHistory, APIStatus)
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API viewsets and views
│   ├── urls.py               # App URL routing
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
├── nse_data.py              # Reusable NSE data fetcher (shared with Flask)
├── db.sqlite3               # SQLite database (created after migrations)
├── manage.py                # Django management script
├── test_api.py              # Comprehensive test suite
├── DJANGO_API_DOCS.md       # API documentation
└── README.md                # Setup guide
```

---

## Installation & Setup

### 1. Prerequisites
```bash
Python 3.8+ installed
pip (Python package manager)
```

### 2. Install Required Packages
```bash
cd NSEDjango

# Core packages
pip install django==5.1.5
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install django-filter==24.1
pip install requests==2.32.3

# Or use requirements.txt (to be created)
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create migrations (if not already done)
python manage.py makemigrations api

# Apply migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser
```

### 4. Load Initial Data
```bash
# Load 139 NSE indices into database
python manage.py load_nse_data
```

Output:
```
Loading NSE data...
Successfully loaded 139 indices (139 new)
```

### 5. Start Development Server
```bash
# Default: http://localhost:8000
python manage.py runserver

# Custom port
python manage.py runserver 0.0.0.0:8000

# Accessible from other machines
python manage.py runserver 0.0.0.0:8000
```

---

## Configuration

### Django Settings (nse_project/settings.py)

**INSTALLED_APPS:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'api',
]
```

**MIDDLEWARE:**
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]
```

**REST Framework Configuration:**
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
```

**CORS Configuration:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Angular frontend
    "http://localhost:4200",      # Angular CLI default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4200",
]
```

---

## API Testing

### Quick Test Commands

**1. Health Check**
```bash
curl http://localhost:8000/api/status/health/
```

**2. API Status**
```bash
curl http://localhost:8000/api/status/status/
```

**3. List Indices**
```bash
curl http://localhost:8000/api/indices/

# With pagination
curl "http://localhost:8000/api/indices/?page=1"

# With search
curl "http://localhost:8000/api/indices/?search=NIFTY"

# With sorting
curl "http://localhost:8000/api/indices/?ordering=-percent_change"
```

**4. Get Single Index**
```bash
curl "http://localhost:8000/api/indices/NIFTY%2050/"
```

**5. Refresh Data**
```bash
curl "http://localhost:8000/api/indices/refresh/"
```

### Run Comprehensive Test Suite
```bash
python test_api.py
```

This runs 25+ test cases covering:
- Health checks
- Basic operations
- Single item retrieval
- Search functionality
- Filtering
- Ordering/sorting
- Complex queries
- Refresh operations
- Historical data
- Error handling

---

## Database Models

### Index Model
Stores current state of all NSE indices with:
- Basic info: name, symbol, key
- Price data: last, open, high, low, previous_close
- Metrics: change, percent_change, year_high, year_low
- Valuations: pe_ratio, pb_ratio, dividend_yield
- Market breadth: advances, declines, unchanged
- Period returns: change_30d, change_365d
- Timestamps: last_updated, created_at

### IndexHistory Model
Tracks historical price data:
- index (ForeignKey)
- timestamp
- price
- change
- percent_change

### APIStatus Model
Monitors endpoint health:
- name
- endpoint
- status (working/blocked/error)
- message
- last_checked

---

## Admin Interface

### Access Admin Panel
```
http://localhost:8000/admin
```

**Login with superuser credentials** (created during setup)

**Available admin sections:**
- Indices (view, edit, delete)
- Index History (view, filter by index)
- API Status (monitor endpoints)

---

## Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/indices/` | List all indices (paginated) |
| GET | `/api/indices/{symbol}/` | Get specific index details |
| GET | `/api/indices/refresh/` | Refresh all indices from NSE |
| GET | `/api/indices/{symbol}/history/` | Get index historical data |
| GET | `/api/history/` | List all historical records |
| GET | `/api/status/status/` | Get API status |
| GET | `/api/status/health/` | Health check |

---

## Common Tasks

### Refresh NSE Data Regularly
```bash
# Manual refresh
curl http://localhost:8000/api/indices/refresh/

# Automated (using cron job or Celery)
python manage.py load_nse_data
```

### Search Indices
```bash
# By name
curl "http://localhost:8000/api/indices/?search=NIFTY"

# By symbol
curl "http://localhost:8000/api/indices/?search=NIFTY%20BANK"

# By key
curl "http://localhost:8000/api/indices/?search=BROAD%20MARKET"
```

### Sort Results
```bash
# Ascending
curl "http://localhost:8000/api/indices/?ordering=name"

# Descending
curl "http://localhost:8000/api/indices/?ordering=-percent_change"
```

### Pagination
```bash
# Get page 1
curl "http://localhost:8000/api/indices/?page=1"

# Get page 3
curl "http://localhost:8000/api/indices/?page=3"

# Custom page size (modify REST_FRAMEWORK['PAGE_SIZE'])
```

---

## Production Deployment

### 1. Prepare for Production
```bash
# Disable debug mode
DEBUG = False

# Set allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use environment variables for secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Configure static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use PostgreSQL instead of SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nse_db',
        'USER': 'nse_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. Run Migrations
```bash
python manage.py migrate
python manage.py load_nse_data
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### 4. Deploy with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn nse_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 5. Use Nginx as Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/NSEDjango/staticfiles/;
    }
}
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port
python manage.py runserver 0.0.0.0:8001

# Or kill existing process
lsof -i :8000
kill -9 <PID>
```

### Database Locked
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py load_nse_data
```

### CORS Errors
```python
# Add frontend URL to CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular
]
```

### NSE API Connection Issues
```bash
# Test connection
python -c "from nse_data import NSEDataFetcher; f = NSEDataFetcher(); print(len(f.get_all_indices().get('data', [])))"

# If returns 139, API is working
```

---

## Integration with Angular Frontend

### 1. Configure Angular Environment
```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

### 2. Create Angular Service
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({providedIn: 'root'})
export class IndexService {
  constructor(private http: HttpClient) {}

  getIndices(page: number = 1): Observable<any> {
    const params = new HttpParams().set('page', page.toString());
    return this.http.get(`${env.apiUrl}/indices/`, {params});
  }

  searchIndices(query: string): Observable<any> {
    const params = new HttpParams().set('search', query);
    return this.http.get(`${env.apiUrl}/indices/`, {params});
  }

  getIndexBySymbol(symbol: string): Observable<any> {
    return this.http.get(`${env.apiUrl}/indices/${symbol}/`);
  }
}
```

### 3. Add HttpClientModule
```typescript
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [HttpClientModule],
})
export class AppModule { }
```

---

## Performance Optimization

### 1. Database Indexes
Already configured on frequently queried fields:
- name
- symbol
- timestamp

### 2. API Caching (Client-Side)
```typescript
// Cache indices in Angular service
private indicesCache: any;

getIndices(): Observable<any> {
  if (this.indicesCache) {
    return of(this.indicesCache);
  }
  return this.http.get(`${env.apiUrl}/indices/`).pipe(
    tap(data => this.indicesCache = data)
  );
}
```

### 3. Pagination
Always use pagination to reduce payload size:
```bash
# Good (50 items per page)
curl "http://localhost:8000/api/indices/?page=1"

# Avoid (all 139 items)
curl "http://localhost:8000/api/indices/refresh/"
```

### 4. Selective Field Retrieval
Request only needed fields using DRF serializers.

---

## Next Steps

1. **✅ Django API Setup** - Complete
2. **✅ Database Models** - Complete
3. **✅ REST Endpoints** - Complete
4. **→ Angular Frontend** - Next phase
5. → End-to-end testing
6. → Production deployment

---

## Useful Commands

```bash
# Create new app
python manage.py startapp new_app

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load data
python manage.py load_nse_data

# Access shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Reset migrations
python manage.py migrate api zero

# Delete all data and recreate
rm db.sqlite3
python manage.py migrate
python manage.py load_nse_data
```

---

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- NSE API: https://www.nseindia.com/
- Angular Documentation: https://angular.io/

---

**Last Updated:** July 4, 2026
**Django Version:** 5.1.5
**DRF Version:** 3.14.0
**Status:** Ready for Angular Integration ✅
