"""
NSE Data Fetcher - Reusable module for fetching NSE indices
Compatible with both Flask and Django
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class NSEDataFetcher:
    BASE_URL = "https://www.nseindia.com/api/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        # Get cookies from NSE homepage to bypass bot protection
        try:
            self.session.get('https://www.nseindia.com', timeout=10)
        except Exception as e:
            print(f"Warning: Could not get NSE cookies: {e}")

    def get_equity_stock_quote(self, symbol):
        """
        IMPORTANT: NSE has blocked direct API access to individual stock quotes.
        The quote-equity endpoint returns 403 Forbidden (Access Denied).
        """
        try:
            url = f"{self.BASE_URL}quote-equity?symbol={symbol}"
            resp = self.session.get(url, headers=self.HEADERS, timeout=10)
            
            if resp.status_code == 403:
                return {
                    'symbol': symbol,
                    'status': 'blocked',
                    'error': 'Direct API access blocked',
                    'message': 'NSE has blocked direct API access to equity stock quotes (HTTP 403)',
                    'recommendation': 'Use get_index_data() to fetch index data, or use alternative data sources',
                    'alternative_endpoint': 'allIndices endpoint is available for index data'
                }
            elif resp.status_code == 200:
                return resp.json()
            else:
                return {
                    'symbol': symbol,
                    'status': 'error',
                    'http_status': resp.status_code,
                    'message': f'Failed to fetch data: HTTP {resp.status_code}'
                }
                
        except Exception as e:
            return {
                'symbol': symbol,
                'status': 'error',
                'error': str(e),
                'message': f'Exception occurred while fetching {symbol}: {str(e)}',
                'note': 'NSE API access is restricted. Consider using alternative data sources.'
            }

    def get_index_data(self, index_name="NIFTY 50"):
        """
        Fetch index data using the working allIndices endpoint.
        This is the ONLY publicly available NSE API endpoint that works.
        """
        url = "https://www.nseindia.com/api/allIndices"
        resp = self.session.get(url, headers=self.HEADERS, timeout=10)
        
        if resp.status_code == 200 and resp.headers.get('Content-Type', '').startswith('application/json'):
            data = resp.json()
            
            # Search for the requested index
            for idx in data.get('data', []):
                if idx.get('index') == index_name:
                    return idx
            
            # Index not found, provide available indices
            available = [idx.get('index') for idx in data.get('data', [])]
            raise Exception(f"Index '{index_name}' not found. Available: {len(available)} indices")
        else:
            raise Exception(f"Failed to fetch index data: {resp.status_code}")
    
    def get_all_indices(self):
        """
        Fetch data for ALL available indices.
        
        Returns:
            dict: Complete response with all indices data
        """
        url = "https://www.nseindia.com/api/allIndices"
        resp = self.session.get(url, headers=self.HEADERS, timeout=10)
        
        if resp.status_code == 200 and resp.headers.get('Content-Type', '').startswith('application/json'):
            return resp.json()
        else:
            raise Exception(f"Failed to fetch data: {resp.status_code}")
