"""
Unit tests for the NSE API.

These run fully offline (no live server, no network): the NSE fetcher is
mocked, so ``python manage.py test`` exercises models, serializers, the
service layer and the DRF endpoints in isolation.
"""
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Index, IndexHistory
from . import services


SAMPLE_NSE_RESPONSE = {
    'timestamp': '04-Jul-2026 15:30',
    'data': [
        {
            'index': 'NIFTY 50', 'indexSymbol': 'NIFTY 50', 'key': 'BROAD MARKET INDICES',
            'last': '24270.85', 'open': '24175.70', 'high': '24286.30', 'low': '24134.25',
            'previousClose': '24175.70', 'variation': '95.15', 'percentChange': '0.39',
            'yearHigh': '24900.00', 'yearLow': '19800.00', 'pe': '23.45', 'pb': '3.20',
            'dy': '1.85', 'advances': '32', 'declines': '18', 'unchanged': '0',
            'perChange30d': '2.15', 'perChange365d': '18.50',
        },
        {
            'index': 'NIFTY BANK', 'indexSymbol': 'NIFTY BANK', 'key': 'BROAD MARKET INDICES',
            'last': '52000.00', 'open': '51800.00', 'high': '52100.00', 'low': '51700.00',
            'previousClose': '51900.00', 'variation': '100.00', 'percentChange': '0.19',
            'yearHigh': '54000.00', 'yearLow': '42000.00', 'pe': '18.10', 'pb': '2.90',
            'dy': '0.95', 'advances': '8', 'declines': '4', 'unchanged': '0',
            'perChange30d': '1.10', 'perChange365d': '12.30',
        },
    ],
}


def _make_index(**overrides):
    defaults = dict(
        name='NIFTY 50', symbol='NIFTY 50', key='BROAD MARKET INDICES',
        last_price=Decimal('24270.85'), change=Decimal('95.15'),
        percent_change=Decimal('0.39'),
    )
    defaults.update(overrides)
    return Index.objects.create(**defaults)


class ModelTests(APITestCase):
    def test_index_str(self):
        index = _make_index()
        self.assertIn('NIFTY 50', str(index))

    def test_index_history_str(self):
        index = _make_index()
        history = IndexHistory.objects.create(index=index, price=Decimal('24270.85'))
        self.assertIn('NIFTY 50', str(history))

    def test_history_related_name(self):
        index = _make_index()
        IndexHistory.objects.create(index=index, price=Decimal('1'))
        IndexHistory.objects.create(index=index, price=Decimal('2'))
        self.assertEqual(index.history.count(), 2)


class ServiceTests(APITestCase):
    @patch('api.services.NSEDataFetcher')
    def test_sync_creates_indices_and_history(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = SAMPLE_NSE_RESPONSE

        result = services.sync_indices(record_history=True)

        self.assertEqual(result['created'], 2)
        self.assertEqual(result['updated'], 0)
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['timestamp'], '04-Jul-2026 15:30')
        self.assertEqual(Index.objects.count(), 2)
        # One history snapshot per index.
        self.assertEqual(IndexHistory.objects.count(), 2)

        nifty = Index.objects.get(symbol='NIFTY 50')
        self.assertEqual(nifty.last_price, Decimal('24270.85'))
        self.assertEqual(nifty.advances, 32)

    @patch('api.services.NSEDataFetcher')
    def test_sync_second_run_updates_not_creates(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = SAMPLE_NSE_RESPONSE
        services.sync_indices()
        result = services.sync_indices()

        self.assertEqual(result['created'], 0)
        self.assertEqual(result['updated'], 2)
        self.assertEqual(Index.objects.count(), 2)
        self.assertEqual(IndexHistory.objects.count(), 4)

    @patch('api.services.NSEDataFetcher')
    def test_sync_without_history(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = SAMPLE_NSE_RESPONSE
        services.sync_indices(record_history=False)
        self.assertEqual(IndexHistory.objects.count(), 0)

    @patch('api.services.NSEDataFetcher')
    def test_sync_invalid_response_raises(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = {'unexpected': True}
        with self.assertRaises(ValueError):
            services.sync_indices()


class IndexEndpointTests(APITestCase):
    def setUp(self):
        _make_index(name='NIFTY 50', symbol='NIFTY 50',
                    last_price=Decimal('24270.85'), percent_change=Decimal('0.39'))
        _make_index(name='NIFTY BANK', symbol='NIFTY BANK',
                    last_price=Decimal('52000.00'), percent_change=Decimal('0.19'))
        _make_index(name='NIFTY IT', symbol='NIFTY IT',
                    last_price=Decimal('38000.00'), percent_change=Decimal('-0.50'))

    def test_list_indices(self):
        resp = self.client.get('/api/indices/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 3)

    def test_retrieve_by_symbol(self):
        resp = self.client.get('/api/indices/NIFTY 50/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['symbol'], 'NIFTY 50')

    def test_retrieve_missing_returns_404(self):
        resp = self.client.get('/api/indices/DOES_NOT_EXIST/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_search(self):
        resp = self.client.get('/api/indices/?search=BANK')
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['symbol'], 'NIFTY BANK')

    def test_ordering(self):
        resp = self.client.get('/api/indices/?ordering=-percent_change')
        changes = [r['percent_change'] for r in resp.data['results']]
        self.assertEqual(changes, sorted(changes, reverse=True))

    def test_history_action_empty(self):
        resp = self.client.get('/api/indices/NIFTY 50/history/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_history_action_with_data(self):
        index = Index.objects.get(symbol='NIFTY 50')
        IndexHistory.objects.create(index=index, price=Decimal('24000.00'))
        resp = self.client.get('/api/indices/NIFTY 50/history/')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['index_name'], 'NIFTY 50')

    @patch('api.services.NSEDataFetcher')
    def test_refresh_action(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = SAMPLE_NSE_RESPONSE
        resp = self.client.get('/api/indices/refresh/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'success')
        # NIFTY 50 / NIFTY BANK already existed -> updated; totals stay consistent.
        self.assertEqual(resp.data['total'], Index.objects.count())


class HistoryEndpointTests(APITestCase):
    def setUp(self):
        self.index = _make_index()
        IndexHistory.objects.create(index=self.index, price=Decimal('24000.00'))
        IndexHistory.objects.create(index=self.index, price=Decimal('24100.00'))

    def test_list_history(self):
        resp = self.client.get('/api/history/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 2)

    def test_filter_history_by_index(self):
        resp = self.client.get(f'/api/history/?index={self.index.id}')
        self.assertEqual(resp.data['count'], 2)


class StatusEndpointTests(APITestCase):
    def test_health(self):
        resp = self.client.get('/api/status/health/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'healthy')

    @patch('api.views.NSEDataFetcher')
    def test_status(self, mock_fetcher_cls):
        mock_fetcher_cls.return_value.get_all_indices.return_value = SAMPLE_NSE_RESPONSE
        resp = self.client.get('/api/status/status/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'operational')
        self.assertEqual(resp.data['available_indices'], 2)
