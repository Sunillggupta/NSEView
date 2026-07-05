"""
Service layer for syncing NSE data into the database.

Centralises the fetch-and-store logic that was previously duplicated between
the ``refresh`` API action and the ``load_nse_data`` management command, and
adds historical tracking (an ``IndexHistory`` row per index on every sync).
"""
from decimal import Decimal, InvalidOperation

from .models import Index, IndexHistory
from NSEView.NSEDjango.nse_data import NSEDataFetcher


def _to_decimal(value, default='0'):
    """Safely convert an NSE field to Decimal, falling back to ``default``."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)


def _to_int(value, default=0):
    """Safely convert an NSE field to int."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def sync_indices(record_history=True):
    """
    Fetch all indices from NSE and upsert them into the database.

    Args:
        record_history: When True, append an ``IndexHistory`` row for each
            index so the history endpoints have data to serve.

    Returns:
        dict with ``created``, ``updated``, ``total`` counts and the source
        ``timestamp`` reported by NSE.
    """
    fetcher = NSEDataFetcher()
    data = fetcher.get_all_indices()

    if not isinstance(data, dict) or 'data' not in data:
        raise ValueError('Invalid response format from NSE API')

    created_count = 0
    updated_count = 0
    history_rows = []

    for item in data.get('data', []):
        symbol = item.get('indexSymbol') or item.get('index')
        if not symbol:
            continue

        last_price = _to_decimal(item.get('last'))
        change = _to_decimal(item.get('variation'))
        percent_change = _to_decimal(item.get('percentChange'))

        index, created = Index.objects.update_or_create(
            symbol=symbol,
            defaults={
                'name': item.get('index'),
                'key': item.get('key'),
                'last_price': last_price,
                'open_price': _to_decimal(item.get('open')),
                'high_price': _to_decimal(item.get('high')),
                'low_price': _to_decimal(item.get('low')),
                'previous_close': _to_decimal(item.get('previousClose')),
                'change': change,
                'percent_change': percent_change,
                'year_high': _to_decimal(item.get('yearHigh')),
                'year_low': _to_decimal(item.get('yearLow')),
                'pe_ratio': str(item.get('pe', 'N/A')),
                'pb_ratio': str(item.get('pb', 'N/A')),
                'dividend_yield': str(item.get('dy', 'N/A')),
                'advances': _to_int(item.get('advances')),
                'declines': _to_int(item.get('declines')),
                'unchanged': _to_int(item.get('unchanged')),
                'change_30d': _to_decimal(item.get('perChange30d')),
                'change_365d': _to_decimal(item.get('perChange365d')),
            }
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

        if record_history:
            history_rows.append(IndexHistory(
                index=index,
                price=last_price,
                change=change,
                percent_change=percent_change,
            ))

    if history_rows:
        IndexHistory.objects.bulk_create(history_rows)

    return {
        'created': created_count,
        'updated': updated_count,
        'total': Index.objects.count(),
        'timestamp': data.get('timestamp'),
    }
