---
name: testing
description: Writes and maintains tests for Python code, web interfaces, and SQL queries. Implements unit tests, integration tests, and end-to-end tests. Use when writing tests, improving test coverage, debugging test failures, or setting up testing frameworks.
---

# Testing

## Quick Start

When writing tests:

1. Understand what needs to be tested
2. Choose appropriate test type (unit/integration/e2e)
3. Write test cases
4. Run tests and fix failures
5. Check coverage
6. Refactor if needed

## Python Testing

Use pytest for Python testing. Write test functions starting with `test_`, use fixtures for setup/teardown, parametrize for multiple cases, and mocking for external dependencies.

**Key concepts:**
- Test structure and organization
- Fixtures for shared setup
- Mocking external dependencies
- Testing exceptions
- Integration testing

**See detailed examples:** [python-testing.md](reference/python-testing.md)

## Web Testing

### HTML/CSS Testing

- Test responsive design at different breakpoints
- Test accessibility with Lighthouse
- Test cross-browser compatibility
- Validate HTML markup
- Check CSS specificity issues

**Manual Testing Checklist:**
- [ ] Test on mobile (320px, 375px, 414px)
- [ ] Test on tablet (768px, 1024px)
- [ ] Test on desktop (1280px, 1920px)
- [ ] Test keyboard navigation
- [ ] Test with screen reader
- [ ] Validate HTML markup
- [ ] Check color contrast
- [ ] Test form validation

### Web Application Testing with Playwright

Use Playwright for testing web scrapers and dynamic websites. Always wait for `networkidle` before inspecting DOM.

**Key pattern:** Reconnaissance-Then-Action
1. Navigate and wait for `networkidle`
2. Take screenshot or inspect DOM
3. Identify selectors from rendered state
4. Execute actions with discovered selectors

**Common pitfall:** Don't inspect DOM before waiting for `networkidle` on dynamic apps.

**See detailed examples:** [playwright-testing.md](reference/playwright-testing.md)

### JavaScript Testing (Future)

- Use Jest for unit testing
- Use Cypress for E2E testing
- Test user interactions
- Test error handling
- Test accessibility

**Jest Example (for future JS projects):**
```javascript
// test/utils.test.js
describe('formatDate', () => {
    test('formats date correctly', () => {
        const date = new Date('2025-01-28');
        expect(formatDate(date)).toBe('28 Jan 2025');
    });
    
    test('handles invalid date', () => {
        expect(() => formatDate(null)).toThrow('Invalid date');
    });
});
```

## SQL Testing

Test query performance, correctness, edge cases (NULL values, empty results), and validate query results.

**Key practices:**
- Test query returns expected columns
- Handle NULL values correctly
- Test query performance
- Use fixtures for test data
- Clean up test data after tests

**See detailed examples:** [sql-testing.md](reference/sql-testing.md)

## Test Organization

### Directory Structure

```
project/
├── src/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_unit.py         # Unit tests
│   ├── test_integration.py  # Integration tests
│   └── fixtures/
│       └── test_data.json
└── pytest.ini
```

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Test Naming

- Use descriptive test names
- Follow pattern: `test_<what>_<condition>_<expected_result>`
- Group related tests in classes
- Use docstrings to explain test purpose

**Good Test Names:**
```python
def test_user_creation_with_valid_data_returns_user_id():
    """Test that creating user with valid data returns user ID."""
    pass

def test_user_creation_with_invalid_email_raises_validation_error():
    """Test that creating user with invalid email raises error."""
    pass

def test_get_user_by_id_when_user_exists_returns_user():
    """Test retrieving existing user by ID."""
    pass
```

## Coverage Requirements

### Minimum Coverage

- Aim for 80%+ coverage
- Focus on critical paths
- Test edge cases
- Test error handling
- Don't test implementation details

### Coverage Tools

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html

# Check coverage threshold
pytest --cov=src --cov-fail-under=80
```

### What to Test

**✅ DO Test:**
- Public API functions
- Business logic
- Error handling
- Edge cases
- Integration points

**❌ DON'T Test:**
- Private methods (test through public API)
- Implementation details
- Third-party library code
- Trivial getters/setters
- Framework code

## Debugging Tests

Common issues: test isolation problems, timing issues, mock configuration errors, data cleanup issues.

**Debugging techniques:**
- Use `pytest --pdb` to drop into debugger on failure
- Use `pytest -s` to show print statements
- Add `breakpoint()` for interactive debugging
- Check mock calls and arguments

**See detailed examples:** [python-testing.md](reference/python-testing.md) (Debugging Tests section)

## Integration Testing

Test with real dependencies (databases, APIs) using fixtures for setup and teardown.

**Key practices:**
- Use in-memory databases for testing
- Test service integration with real dependencies
- Clean up test data after tests

**See detailed examples:** [python-testing.md](reference/python-testing.md) (Integration Testing section)

## Best Practices Summary

### Writing Tests
- Write tests before fixing bugs (TDD when possible)
- Keep tests simple and focused
- Use meaningful test names
- Test behavior, not implementation
- One assertion per test (when possible)

### Test Organization
- Group related tests in classes
- Use fixtures for shared setup
- Keep test data in fixtures directory
- Document test requirements
- Maintain test coverage

### Debugging
- Use pytest debugging tools
- Add print statements for debugging
- Check mock calls and arguments
- Verify test data
- Test in isolation

### Maintenance
- Refactor tests regularly
- Remove obsolete tests
- Update tests when code changes
- Keep tests fast
- Document test purpose
