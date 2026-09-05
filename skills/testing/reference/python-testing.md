# Python Testing Reference

## Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from app.module import function_to_test

class TestFunction:
    def setup_method(self):
        """Setup before each test."""
        self.test_data = {"key": "value"}
    
    def test_function_success(self):
        """Test successful execution."""
        result = function_to_test(self.test_data)
        assert result is not None
        assert result["status"] == "success"
    
    def test_function_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            function_to_test(None)
    
    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
    ])
    def test_function_multiple_cases(self, input, expected):
        """Test multiple cases."""
        result = function_to_test(input)
        assert result == expected
```

## Fixtures

```python
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "name": "Test",
        "value": 123,
        "items": [1, 2, 3]
    }

def test_with_fixtures(temp_dir, sample_data):
    """Test using fixtures."""
    test_file = temp_dir / "test.json"
    # Use temp_dir and sample_data
    assert test_file.parent.exists()
    assert sample_data["name"] == "Test"
```

## Mocking External Dependencies

```python
from unittest.mock import Mock, patch, MagicMock

@patch('app.module.external_api_call')
def test_with_mock(mock_api):
    """Test with mocked external API."""
    mock_api.return_value = {"data": "test"}
    result = function_using_api()
    assert result["data"] == "test"
    mock_api.assert_called_once()

@patch('requests.get')
def test_http_request(mock_get):
    """Test HTTP request with mock."""
    mock_response = Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    result = fetch_data_from_api()
    assert result["status"] == "ok"
```

## Testing Exceptions

```python
import pytest
from app.exceptions import CustomError

def test_raises_exception():
    """Test that function raises expected exception."""
    with pytest.raises(CustomError) as exc_info:
        function_that_raises()
    
    assert "expected message" in str(exc_info.value)

def test_raises_specific_exception():
    """Test specific exception type."""
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(None)
```

## Integration Testing

```python
import pytest
from app.database import Database
from app.services import UserService

@pytest.fixture
def test_db():
    """Create test database."""
    db = Database(":memory:")  # SQLite in-memory
    db.create_tables()
    yield db
    db.close()

def test_user_service_integration(test_db):
    """Test user service with real database."""
    service = UserService(test_db)
    
    # Create user
    user_id = service.create_user({
        "name": "Test User",
        "email": "test@example.com"
    })
    
    # Retrieve user
    user = service.get_user(user_id)
    
    assert user is not None
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"
```

## Debugging Tests

**Use pytest debugging:**
```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show print statements
pytest -s
```

**Add debugging to tests:**
```python
def test_complex_function():
    """Test with debugging."""
    result = complex_function()
    
    # Debug output
    print(f"Result: {result}")
    print(f"Result type: {type(result)}")
    
    # Use breakpoint() for interactive debugging
    if result is None:
        breakpoint()  # Drops into debugger
    
    assert result is not None
```

**Check mock calls:**
```python
@patch('app.module.external_call')
def test_mock_calls(mock_call):
    """Test mock was called correctly."""
    function_that_calls_external()
    
    # Check mock was called
    assert mock_call.called
    
    # Check call arguments
    mock_call.assert_called_once_with('expected_arg')
    
    # Check call count
    assert mock_call.call_count == 1
    
    # Inspect call details
    call_args = mock_call.call_args
    print(f"Called with: {call_args}")
```
