---
name: database-analysis
description: Analyzes SQL queries, database schemas, and data structures. Optimizes queries, identifies performance issues, and provides data insights. Use when working with SQL, databases, data analysis, or query optimization.
---

# Database Analysis

## Quick Start

When analyzing databases:

1. Understand the data requirement
2. Examine schema and relationships
3. Write efficient SQL queries
4. Analyze and optimize performance
5. Present findings clearly

## Query Analysis

### Performance Optimization

- Check for missing indexes
- Analyze join types and order
- Review WHERE clause filters
- Identify N+1 query patterns
- Evaluate subquery vs JOIN performance

### Query Structure

- Use CTEs for complex logic
- Format queries for readability
- Add comments for business logic
- Validate data types and constraints
- Handle NULL values appropriately

## Schema Analysis

- Review table relationships
- Check foreign key constraints
- Validate data types
- Identify normalization opportunities
- Assess index coverage

## Common Patterns

### Efficient Filtering

```sql
-- ✅ GOOD: Indexed column in WHERE
SELECT * FROM users WHERE user_id = 123;

-- ❌ BAD: Function on indexed column
SELECT * FROM users WHERE UPPER(email) = 'TEST@EXAMPLE.COM';
```

### Join Optimization

```sql
-- ✅ GOOD: Filter before join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- ❌ BAD: Filter after join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01';
```

## Data Quality Checks

- Identify duplicate records
- Check for NULL values in required fields
- Validate data ranges and constraints
- Assess data completeness
- Review data consistency

## Output Format

For each analysis:
- Explain the query approach
- Document assumptions
- Highlight key findings
- Suggest optimizations
- Provide next steps based on data
