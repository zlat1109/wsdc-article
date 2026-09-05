# Testing Reference

## pytest for Scraping Tests

```python
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
        <body>
            <div class="job-listing">
                <h2 class="title">Python Developer</h2>
                <span class="company">Tech Corp</span>
            </div>
        </body>
    </html>
    """

def test_parse_job_listing(sample_html):
    """Test parsing job listing from HTML."""
    soup = BeautifulSoup(sample_html, 'html.parser')
    listing = soup.select_one('.job-listing')
    
    assert listing is not None
    assert listing.select_one('.title').text == "Python Developer"
    assert listing.select_one('.company').text == "Tech Corp"

@patch('requests.get')
def test_scraper_with_mock(mock_get):
    """Test scraper with mocked HTTP request."""
    mock_response = Mock()
    mock_response.content = b'<html><body>Test</body></html>'
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    result = scrape_page('http://example.com')
    assert result is not None
    mock_get.assert_called_once_with('http://example.com', timeout=10)
```
