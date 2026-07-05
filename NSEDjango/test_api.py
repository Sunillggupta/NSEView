"""
Comprehensive test suite for Django REST API
Tests all endpoints, filtering, searching, and error handling
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"


class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test(self, name: str, method: str, endpoint: str, **kwargs) -> bool:
        """Execute a single test"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, **kwargs)
            success = response.status_code < 400
            
            result = {
                'name': name,
                'status': 'PASS' if success else 'FAIL',
                'method': method,
                'endpoint': endpoint,
                'status_code': response.status_code,
                'data': response.text[:200] if not success else None
            }
            self.test_results.append(result)
            
            status_symbol = "[OK]" if success else "[ERR]"
            print(f"{status_symbol} {name} ({response.status_code})")
            return success
        except Exception as e:
            print(f"[ERR] {name} - {str(e)}")
            self.test_results.append({
                'name': name,
                'status': 'ERROR',
                'error': str(e)
            })
            return False
    
    def print_summary(self):
        """Print test results summary"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = total - passed
        
        print("\n" + "="*60)
        print(f"TEST SUMMARY: {passed}/{total} PASSED")
        print("="*60)
        
        for result in self.test_results:
            status_symbol = "[OK]" if result['status'] == 'PASS' else "[ERR]"
            print(f"{status_symbol} {result['name']}")


def run_all_tests():
    """Run comprehensive test suite"""
    tester = APITester()
    
    print("\n" + "="*60)
    print("DJANGO REST API TEST SUITE")
    print("="*60 + "\n")
    
    # 1. Health Checks
    print("1. HEALTH CHECKS")
    print("-" * 60)
    tester.test("Health check", "GET", "/status/health/")
    tester.test("API status", "GET", "/status/status/")
    
    # 2. Indices - Basic Operations
    print("\n2. INDICES - BASIC OPERATIONS")
    print("-" * 60)
    tester.test("List all indices", "GET", "/indices/")
    tester.test("Get first page", "GET", "/indices/?page=1")
    tester.test("Get second page", "GET", "/indices/?page=2")
    
    # 3. Indices - Single Item
    print("\n3. INDICES - SINGLE ITEM RETRIEVAL")
    print("-" * 60)
    tester.test("Get NIFTY 50", "GET", "/indices/NIFTY%2050/")
    tester.test("Get NIFTY BANK", "GET", "/indices/NIFTY%20BANK/")
    tester.test("Get NIFTY 100", "GET", "/indices/NIFTY%20100/")
    
    # 4. Indices - Search
    print("\n4. INDICES - SEARCH FUNCTIONALITY")
    print("-" * 60)
    tester.test("Search 'NIFTY'", "GET", "/indices/?search=NIFTY")
    tester.test("Search 'BANK'", "GET", "/indices/?search=BANK")
    tester.test("Search 'PSU'", "GET", "/indices/?search=PSU")
    tester.test("Search 'AUTO'", "GET", "/indices/?search=AUTO")
    
    # 5. Indices - Filtering
    print("\n5. INDICES - FILTERING")
    print("-" * 60)
    tester.test("Filter by symbol", "GET", "/indices/?search=NIFTY%2050")
    tester.test("Combine search and page", "GET", "/indices/?search=NIFTY&page=1")
    
    # 6. Indices - Ordering
    print("\n6. INDICES - ORDERING/SORTING")
    print("-" * 60)
    tester.test("Order by name ASC", "GET", "/indices/?ordering=name")
    tester.test("Order by name DESC", "GET", "/indices/?ordering=-name")
    tester.test("Order by price ASC", "GET", "/indices/?ordering=last_price")
    tester.test("Order by price DESC", "GET", "/indices/?ordering=-last_price")
    tester.test("Order by percent change DESC", "GET", "/indices/?ordering=-percent_change")
    
    # 7. Indices - Combined
    print("\n7. INDICES - COMPLEX QUERIES")
    print("-" * 60)
    tester.test("Search + Sort by change", "GET", "/indices/?search=NIFTY&ordering=-percent_change")
    tester.test("Search + Page 2", "GET", "/indices/?search=NIFTY&page=2")
    tester.test("Sort by change + limit", "GET", "/indices/?ordering=-percent_change&page=1")
    
    # 8. Refresh Operation
    print("\n8. INDICES - REFRESH DATA")
    print("-" * 60)
    tester.test("Refresh all indices", "GET", "/indices/refresh/")
    
    # 9. History
    print("\n9. HISTORICAL DATA")
    print("-" * 60)
    tester.test("Get NIFTY 50 history", "GET", "/indices/NIFTY%2050/history/")
    tester.test("List all history", "GET", "/history/")
    tester.test("History page 1", "GET", "/history/?page=1")
    
    # 10. Error Handling
    print("\n10. ERROR HANDLING")
    print("-" * 60)
    tester.test("Non-existent index (404)", "GET", "/indices/INVALID_INDEX/")
    tester.test("Invalid page number", "GET", "/indices/?page=9999")
    
    # Print summary
    tester.print_summary()
    
    return tester


if __name__ == "__main__":
    tester = run_all_tests()
    
    # Additional analysis
    print("\n" + "="*60)
    print("DETAILED ENDPOINT RESPONSES")
    print("="*60)
    
    try:
        # Sample index data
        response = requests.get(f"{BASE_URL}/indices/?page=1")
        data = response.json()
        
        print("\n[Sample] NIFTY 50 Summary:")
        response = requests.get(f"{BASE_URL}/indices/NIFTY%2050/")
        index = response.json()
        print(f"  - Price: {index['last_price']}")
        print(f"  - Change: {index['change']} ({index['percent_change']}%)")
        print(f"  - High: {index['high_price']} | Low: {index['low_price']}")
        print(f"  - P/E Ratio: {index['pe_ratio']}")
        print(f"  - Advances: {index['advances']} | Declines: {index['declines']}")
        
    except Exception as e:
        print(f"Error fetching details: {str(e)}")
