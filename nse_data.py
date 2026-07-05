import requests
from bs4 import BeautifulSoup
import json

class NSEDataFetcher:
    BASE_URL = "https://www.nseindia.com/api/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
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
        self.session.get('https://www.nseindia.com', timeout=10)

    def get_equity_stock_quote(self, symbol):
        """
        IMPORTANT: NSE has blocked direct API access to individual stock quotes.
        The quote-equity endpoint returns 403 Forbidden (Access Denied).
        
        This method attempts to fetch equity data but will return an informative
        message about the limitation. For actual equity data, use get_index_data()
        or alternative data sources.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'TCS')
            
        Returns:
            dict: Contains status information and limitations
        """
        try:
            # Try the direct API first (will return 403)
            url = f"{self.BASE_URL}quote-equity?symbol={symbol}"
            resp = self.session.get(url, headers=self.HEADERS, timeout=10)
            
            if resp.status_code == 403:
                # API is blocked
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
        
        Args:
            index_name: Name of the index (default: 'NIFTY 50')
            
        Returns:
            dict: Contains index data with latest price, change, volume, etc.
            
        Raises:
            Exception: If the index is not found or API fails
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
            raise Exception(f"Index '{index_name}' not found. Available indices: {', '.join(available[:10])}...")
        else:
            raise Exception(f"Failed to fetch index data: {resp.status_code} {resp.text}")
    
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
            raise Exception(f"Failed to fetch data: {resp.status_code} {resp.text}")




def test_data():
    fetcher = NSEDataFetcher()
    try:
        quote = fetcher.get_equity_stock_quote("RELIANCE")
        print("Equity Stock Quote:")
        print(quote)

        index_data = fetcher.get_index_data("NIFTY 50")
        print("\nIndex Data:")
        print(index_data)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_data()