# Playwright Testing Reference

## Web Application Testing with Playwright

**For testing web scrapers and dynamic websites:**

```python
from playwright.sync_api import sync_playwright

def test_web_scraper():
    """Test web scraper with Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate and wait for content
        page.goto('https://example.com')
        page.wait_for_load_state('networkidle')  # CRITICAL: Wait for JS
        
        # Take screenshot for debugging
        page.screenshot(path='debug.png', full_page=True)
        
        # Inspect DOM
        content = page.content()
        buttons = page.locator('button').all()
        
        # Test scraping logic
        title = page.locator('h1').first().inner_text()
        assert title is not None
        
        browser.close()
```

## Reconnaissance-Then-Action Pattern

1. Navigate and wait for `networkidle`
2. Take screenshot or inspect DOM
3. Identify selectors from rendered state
4. Execute actions with discovered selectors

**Common Pitfall:**
- ❌ Don't inspect DOM before waiting for `networkidle` on dynamic apps
- ✅ Always wait for `page.wait_for_load_state('networkidle')` before inspection

## Testing Static HTML

```python
# For static HTML files, read directly
from pathlib import Path
from bs4 import BeautifulSoup

def test_static_html():
    """Test static HTML file."""
    html_file = Path('index.html')
    soup = BeautifulSoup(html_file.read_text(), 'html.parser')
    
    # Identify selectors
    buttons = soup.select('button')
    assert len(buttons) > 0
```
