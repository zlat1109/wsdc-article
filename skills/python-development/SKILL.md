---
name: python-development
description: Develops Python applications including web scraping, data processing, API integration, and automation. Implements PEP standards, error handling, and testing. Use when working with Python code, web scraping, data parsing, API development, or Python automation tasks.
---

# Python Development

## Quick Start

When developing Python applications:

1. Set up virtual environment
2. Install dependencies
3. Write code following PEP standards
4. Implement error handling
5. Add type hints
6. Write tests
7. Document code

## Environment Setup

### Virtual Environment

**Always use virtual environments:**
```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Project Structure

```
project/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py
│   ├── scrapers/          # Web scraping modules
│   ├── parsers/           # Data parsing modules
│   ├── utils/             # Utility functions
│   └── models/            # Data models
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_scrapers.py
│   └── test_parsers.py
├── data/                   # Data files
├── logs/                   # Log files
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── .gitignore
└── README.md
```

## Code Quality Standards

### PEP 8 Compliance

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use meaningful variable and function names
- Follow naming conventions (snake_case for functions/variables, PascalCase for classes)
- Use blank lines appropriately

**Example:**
```python
# ✅ GOOD
def scrape_job_listings(url: str, max_pages: int = 10) -> List[Dict[str, Any]]:
    """Scrape job listings from URL.
    
    Args:
        url: Base URL to scrape
        max_pages: Maximum number of pages to scrape
        
    Returns:
        List of job listing dictionaries
    """
    listings = []
    # Implementation
    return listings

# ❌ BAD
def scrape(url,max=10):
    l=[]
    # implementation
    return l
```

### Type Hints (PEP 484)

**Always use type hints:**
```python
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

def process_data(
    data: List[Dict[str, Any]],
    filter_func: Optional[callable] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Process data with optional filtering."""
    if filter_func:
        data = [item for item in data if filter_func(item)]
    return {"processed": data}

class JobListing:
    def __init__(
        self,
        title: str,
        company: str,
        location: str,
        salary: Optional[str] = None,
        posted_date: Optional[datetime] = None
    ):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.posted_date = posted_date or datetime.now()
```

## Web Scraping

Use BeautifulSoup for static HTML, Requests for HTTP, Selenium/Playwright for JavaScript-heavy sites.

**Key libraries:**
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `selenium` or `playwright` - JavaScript rendering
- `httpx` - Async HTTP (alternative to requests)

**Best practices:**
- Respect robots.txt
- Implement rate limiting
- Use proper User-Agent headers
- Handle errors gracefully
- Cache responses when possible

**See detailed examples:** [web-scraping.md](reference/web-scraping.md)

## Data Processing

Use Pandas for data manipulation, Pydantic for data validation.

**Key libraries:**
- `pandas` - Data manipulation and analysis
- `pydantic` - Data validation with type hints

**Common operations:**
- Clean and normalize data
- Handle missing values
- Convert data types
- Remove duplicates
- Validate with Pydantic models

**See detailed examples:** [data-processing.md](reference/data-processing.md)

## Error Handling

Implement comprehensive error handling with logging and retry logic.

**Key practices:**
- Use try-except appropriately
- Log errors with context
- Implement retry logic for transient failures
- Validate input data
- Provide meaningful error messages

**Libraries:**
- `logging` - Built-in logging
- `tenacity` - Retry decorators

**See detailed examples:** [error-handling.md](reference/error-handling.md)

## API Integration

Create REST API clients with proper error handling and authentication.

**Key patterns:**
- Use `requests.Session()` for connection pooling
- Implement authentication (Bearer tokens, API keys)
- Handle errors gracefully
- Support GET, POST, PUT, DELETE methods

**See detailed examples:** [api-integration.md](reference/api-integration.md)

## Telegram Bot Development

Use `python-telegram-bot` library for Telegram bot development.

**Key concepts:**
- Application builder pattern
- Command handlers
- Message handlers
- Async/await for handlers

**See detailed examples:** [api-integration.md](reference/api-integration.md) (Telegram section)

## Testing

Use pytest for Python testing. Mock external dependencies, test error cases.

**Key practices:**
- Write unit tests for core functions
- Mock external dependencies (HTTP requests, APIs)
- Test error cases
- Maintain test coverage > 80%
- Use fixtures for test data

**See detailed examples:** [testing.md](reference/testing.md)

## Configuration Management

Use environment variables with `python-dotenv` for configuration.

**Key practices:**
- Store secrets in `.env` file (never commit)
- Use Config class for type-safe access
- Validate required configuration on startup
- Provide sensible defaults

**See detailed examples:** [configuration.md](reference/configuration.md)

## Logging Best Practices

Configure logging with file rotation and console output.

**Key practices:**
- Use RotatingFileHandler for log files
- Set appropriate log levels
- Format logs with timestamps and context
- Log errors with stack traces

**See detailed examples:** [error-handling.md](reference/error-handling.md) (Logging section)

## Best Practices Summary

### Code Quality
- Follow PEP 8 standards
- Use type hints (PEP 484)
- Write docstrings (Google style)
- Keep functions small and focused
- Use meaningful names

### Web Scraping
- Respect robots.txt
- Implement rate limiting
- Use proper User-Agent headers
- Handle errors gracefully
- Cache responses when possible

### Error Handling
- Use try-except appropriately
- Log errors with context
- Implement retry logic
- Validate input data
- Provide meaningful error messages

### Testing
- Write unit tests for core functions
- Mock external dependencies
- Test error cases
- Maintain test coverage > 80%
- Use fixtures for test data

### Performance
- Use connection pooling (requests.Session)
- Implement caching
- Process data in batches
- Use generators for large datasets
- Profile code for bottlenecks
