# Error Handling Reference

## Comprehensive Error Handling

```python
import logging
from typing import Optional, Any
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def handle_errors(func):
    """Decorator for error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error in {func.__name__}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            return None
    return wrapper

@handle_errors
def scrape_with_error_handling(url: str) -> Optional[List[Dict]]:
    """Scrape with comprehensive error handling."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    # Process response
    return processed_data
```

## Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_with_retry(url: str) -> requests.Response:
    """Fetch URL with exponential backoff retry."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response
```

## Logging Best Practices

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_dir: Path = Path('logs')):
    """Setup logging configuration."""
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s')
    )
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```
