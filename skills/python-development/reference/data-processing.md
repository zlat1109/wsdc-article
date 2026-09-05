# Data Processing Reference

## Pandas for Data Manipulation

```python
import pandas as pd
from typing import List, Dict

def process_scraped_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Process scraped data into DataFrame."""
    df = pd.DataFrame(data)
    
    # Clean data
    df['title'] = df['title'].str.strip()
    df['company'] = df['company'].str.strip()
    
    # Handle missing values
    df['salary'] = df['salary'].fillna('Not specified')
    
    # Convert dates
    df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['title', 'company', 'location'])
    
    return df

def save_to_csv(df: pd.DataFrame, filename: str):
    """Save DataFrame to CSV."""
    df.to_csv(filename, index=False, encoding='utf-8')
```

## Data Validation with Pydantic

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class JobListing(BaseModel):
    """Job listing data model."""
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1)
    salary: Optional[str] = None
    description: Optional[str] = None
    url: str = Field(..., regex=r'^https?://')
    posted_date: Optional[datetime] = None
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Usage
try:
    job = JobListing(
        title="Python Developer",
        company="Tech Corp",
        location="Remote",
        url="https://example.com/job/123"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```
