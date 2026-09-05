# SQL Testing Reference

## Query Testing

**SQL Test Pattern:**
```python
import pytest
from app.database import execute_query

def test_query_returns_expected_columns():
    """Test that query returns expected columns."""
    result = execute_query("SELECT id, name FROM users LIMIT 1")
    assert len(result) > 0
    assert 'id' in result[0]
    assert 'name' in result[0]

def test_query_handles_null_values():
    """Test query handles NULL values correctly."""
    result = execute_query("""
        SELECT id, COALESCE(name, 'Unknown') as name 
        FROM users 
        WHERE id = 1
    """)
    assert result[0]['name'] is not None

def test_query_performance():
    """Test query performance."""
    import time
    start = time.time()
    execute_query("SELECT * FROM large_table")
    duration = time.time() - start
    assert duration < 1.0  # Should complete in under 1 second
```

## Test Data Management

```python
@pytest.fixture
def test_database():
    """Create test database with sample data."""
    # Setup
    db = create_test_db()
    insert_test_data(db)
    yield db
    # Teardown
    cleanup_test_db(db)

def test_with_test_data(test_database):
    """Test using test database fixture."""
    result = test_database.query("SELECT * FROM users")
    assert len(result) == 5  # Expected test data count
```
