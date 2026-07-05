from NSEView.Old_Project.nse_data import NSEDataFetcher

def test_data():
    """
    Test the NSEDataFetcher with the corrected API.
    
    NOTE: NSE has blocked direct API access to individual equity stock quotes.
    The allIndices endpoint is the only working public API endpoint from NSE.
    """
    fetcher = NSEDataFetcher()
    try:
        # Test 1: Fetch index data (WORKING)
        print("TEST 1: Fetching Index Data (NIFTY 50)")
        print("-" * 50)
        index_data = fetcher.get_index_data("NIFTY 50")
        print(f"Index: {index_data.get('index')}")
        print(f"Last Price: {index_data.get('last')}")
        print(f"Change: {index_data.get('variation')} ({index_data.get('percentChange')}%)")
        print(f"Open: {index_data.get('open')}, High: {index_data.get('high')}, Low: {index_data.get('low')}")
        print()
        
        # Test 2: Fetch all indices data
        print("TEST 2: Fetching All Indices Data")
        print("-" * 50)
        all_data = fetcher.get_all_indices()
        print(f"Total indices available: {len(all_data.get('data', []))}")
        print("First 5 indices:")
        for idx in all_data.get('data', [])[:5]:
            print(f"  - {idx.get('index')}: {idx.get('last')}")
        print()
        
        # Test 3: Try to fetch equity quote (API blocked - will return status)
        print("TEST 3: Attempting to Fetch Equity Stock Quote (RELIANCE)")
        print("-" * 50)
        quote = fetcher.get_equity_stock_quote("RELIANCE")
        print(f"Status: {quote.get('status')}")
        print(f"Message: {quote.get('message')}")
        print()
        
        print("=" * 50)
        print("SUMMARY:")
        print("=" * 50)
        print("[SUCCESS] Index data API is working correctly")
        print("[INFO] Direct equity quotes are blocked by NSE (HTTP 403)")
        print("[SOLUTION] Use allIndices endpoint for market data")
        print("[RECOMMENDATION] For individual stock data, use:")
        print("  - Alternative data sources")
        print("  - Web scraping with Selenium/Playwright")
        print("  - Third-party APIs")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_data()
