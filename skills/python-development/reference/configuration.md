# Configuration Management Reference

## Environment Variables

```python
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    API_KEY: Optional[str] = os.getenv('API_KEY')
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '10'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")
```
