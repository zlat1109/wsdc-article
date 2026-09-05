# Web Scraping Reference

## BeautifulSoup

**HTML parsing with BeautifulSoup:**
```python
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional

def scrape_with_beautifulsoup(url: str) -> List[Dict[str, str]]:
    """Scrape data using BeautifulSoup."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        for element in soup.select('.item-class'):
            item = {
                'title': element.select_one('.title').get_text(strip=True),
                'description': element.select_one('.description').get_text(strip=True),
                'link': element.select_one('a')['href'] if element.select_one('a') else None
            }
            items.append(item)
        
        return items
        
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []
```

## Requests Library

**HTTP requests with error handling:**
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def fetch_page(self, url: str, headers: Optional[Dict] = None) -> Optional[requests.Response]:
        """Fetch page with retry logic."""
        try:
            response = self.session.get(
                url,
                headers=headers or {},
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
```

## Selenium (for JavaScript-heavy sites)

**Selenium web scraping:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict

def scrape_with_selenium(url: str) -> List[Dict[str, str]]:
    """Scrape JavaScript-rendered content with Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    items = []
    
    try:
        driver.get(url)
        
        # Wait for content to load
        wait = WebDriverWait(driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item-class'))
        )
        
        for element in elements:
            item = {
                'title': element.find_element(By.CSS_SELECTOR, '.title').text,
                'description': element.find_element(By.CSS_SELECTOR, '.description').text
            }
            items.append(item)
        
    except TimeoutException:
        print("Timeout waiting for page to load")
    except Exception as e:
        print(f"Error scraping with Selenium: {e}")
    finally:
        driver.quit()
    
    return items
```

## Rate Limiting

**Rate limiting and politeness:**
```python
import time
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    def __init__(self, requests_per_second: float = 1.0):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time: Optional[datetime] = None
    
    def wait_if_needed(self):
        """Wait if needed to respect rate limit."""
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
        self.last_request_time = datetime.now()

# Usage
rate_limiter = RateLimiter(requests_per_second=2.0)

for url in urls:
    rate_limiter.wait_if_needed()
    response = requests.get(url)
    # Process response
```

## User-Agent Rotation

**User-Agent rotation:**
```python
import random
from typing import List

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

def get_random_headers() -> Dict[str, str]:
    """Get random user agent headers."""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
```
