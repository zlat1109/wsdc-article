---
name: code-review
description: Reviews code for quality, security, and maintainability following team standards. Use when reviewing pull requests, examining code changes, or when the user asks for a code review.
---

# Code Review

## Quick Start

When reviewing code:

1. Check for correctness and potential bugs
2. Verify security best practices
3. Assess code readability and maintainability
4. Ensure tests are adequate

## Review Checklist

- [ ] Logic is correct and handles edge cases
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)
- [ ] Code follows project style conventions
- [ ] Functions are appropriately sized and focused
- [ ] Error handling is comprehensive
- [ ] Tests cover the changes
- [ ] Documentation is updated if needed
- [ ] Performance considerations addressed

## Providing Feedback

Format feedback as:
- 🔴 **Critical**: Must fix before merge
- 🟡 **Suggestion**: Consider improving
- 🟢 **Nice to have**: Optional enhancement

## Python-Specific Checks

- Type hints used appropriately
- PEP 8 compliance
- No bare `except:` clauses
- Proper error handling and logging
- Docstrings for public functions/classes

## SQL-Specific Checks

- Query performance (indexes, joins)
- SQL injection prevention (parameterized queries)
- Data type validation
- Query readability and formatting
- Business logic correctness

## Security Focus Areas

- Input validation
- Authentication/authorization
- Sensitive data handling
- API security
- Dependency vulnerabilities
