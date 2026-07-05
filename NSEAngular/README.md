# NSE Data Dashboard — Angular UI

Angular 19 single-page app that replaces the original Flask/Jinja UI (`../NSEView`)
and consumes the Django REST API (`../NSEDjango`).

## Architecture

```
NSEAngular (Angular 19, :4200)  ──HTTP──▶  NSEDjango (DRF API, :8000)  ──▶  NSE allIndices
```

The API base URL is configured in `src/environments/environment*.ts`
(`apiUrl: 'http://localhost:8000/api'`).

## Pages / routes

| Route             | Component            | Replaces (Flask)          |
| ----------------- | -------------------- | ------------------------- |
| `/`               | `DashboardComponent` | `index.html`              |
| `/index/:symbol`  | `IndexDetailComponent` | `index_detail.html`     |
| `/about`          | `AboutComponent`     | `about.html`              |
| `/status`         | `StatusComponent`    | `/api/status` JSON view   |

Search, category filters (All / Derivatives / Broad Market), and the price-change
colouring from the original templates are all preserved. Added on top: a
"Refresh from NSE" button (calls `/api/indices/refresh/`), an API status page, and
a per-index history table.

## Running the full stack

**1. Backend (Django API):**

```bash
cd ../NSEDjango
python manage.py migrate
python manage.py load_nse_data      # populate the DB from NSE
python manage.py runserver 8000
```

**2. Frontend (this app):**

```bash
npm install        # first time only
npm start          # ng serve, http://localhost:4200
```

CORS for `http://localhost:4200` is already allow-listed in the Django settings.

## Build

```bash
npm run build      # production build to dist/nseangular
```
