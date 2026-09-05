---
name: tableau-workflows
description: Works with Tableau workbooks, dashboards, and data sources. Creates visualizations, optimizes performance, and manages Tableau projects. Use when working with Tableau, .twb/.twbx files, dashboards, or data visualization.
---

# Tableau Workflows

## Quick Start

When working with Tableau:

1. Understand the visualization goal
2. Prepare and validate data sources
3. Design efficient data model
4. Create optimized calculations
5. Build performant dashboards

## Data Preparation

### Data Source Best Practices

- Use extracts (.hyper) for large datasets
- Optimize data source filters
- Remove unused fields
- Set appropriate data types
- Configure relationships correctly

### Performance Optimization

- Use data source filters instead of dashboard filters when possible
- Limit data to necessary date ranges
- Aggregate at data source level
- Use incremental refresh for extracts
- Optimize calculated fields

## Calculated Fields

### Efficient Calculations

```tableau
// ✅ GOOD: Simple calculation
[Sales] * [Quantity]

// ❌ BAD: Complex nested IF
IF [Category] = "A" THEN 
  IF [Subcategory] = "X" THEN [Sales] * 1.1 
  ELSE [Sales] 
END
ELSE [Sales]
END
```

### Best Practices

- Avoid row-level calculations in large datasets
- Use LOD expressions for aggregations
- Cache frequently used calculations
- Document complex business logic
- Test calculations with sample data

## Dashboard Design

### Layout Optimization

- Use containers for responsive layouts
- Minimize number of worksheets
- Optimize filter placement
- Use actions instead of multiple filters
- Test on different screen sizes

### Performance Tips

- Limit data points in views
- Use appropriate chart types
- Avoid over-filtering
- Optimize tooltips
- Use images sparingly

## Common Workflows

### Creating New Dashboard

1. Define metrics and KPIs
2. Select appropriate chart types
3. Design layout structure
4. Add filters and actions
5. Test interactivity
6. Optimize performance

### Optimizing Existing Dashboard

1. Analyze performance metrics
2. Identify slow worksheets
3. Review data source configuration
4. Optimize calculations
5. Test improvements

## Data Integration

### Python Integration

- Use TabPy for advanced analytics
- Prepare Python scripts for Tableau
- Handle data transformations
- Manage dependencies

### SQL Integration

- Write efficient custom SQL
- Use parameters for flexibility
- Optimize query performance
- Handle connection pooling

## Excel Data Preparation

### Working with Excel Files

**CRITICAL: Use Excel formulas, not hardcoded values**

```python
# ❌ WRONG - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# ✅ CORRECT - Using Excel formulas
sheet['B10'] = '=SUM(B2:B9)'  # Excel calculates dynamically
```

### Excel Libraries

**For data analysis:**
```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)

# Analyze
df.head()
df.info()
df.describe()

# Write Excel
df.to_excel('output.xlsx', index=False)
```

**For formulas and formatting:**
```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create workbook
wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Revenue'
sheet['B1'] = '=SUM(B2:B10)'  # Formula, not hardcoded value

# Formatting
sheet['A1'].font = Font(bold=True)
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

wb.save('output.xlsx')
```

### Excel Best Practices

**Number Formatting:**
- Years: Format as text strings ("2024" not "2,024")
- Currency: Use $#,##0 format with units in headers
- Zeros: Display as "-" using number formatting
- Percentages: Default to 0.0% format
- Negative numbers: Use parentheses (123) not minus -123

**Formula Construction:**
- Place ALL assumptions in separate cells
- Use cell references instead of hardcoded values
- Verify all cell references are correct
- Test with edge cases (zero, negative values)
- Document data sources for hardcoded values

**Example:**
```python
# Good: Assumptions in separate cells
sheet['B6'] = 0.05  # Growth rate assumption
sheet['B5'] = '=B4*(1+$B$6)'  # Formula using assumption

# Bad: Hardcoded in formula
sheet['B5'] = '=B4*1.05'  # Hardcoded growth rate
```

## PDF Data Extraction

### Extracting Tables from PDF

**For Tableau data preparation:**

```python
import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path: str) -> pd.DataFrame:
    """Extract tables from PDF for Tableau import."""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:  # Has header and data
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)
    
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        return combined_df
    return pd.DataFrame()
```

### PDF Text Extraction

```python
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
```

### Converting PDF Tables to Excel

```python
def pdf_tables_to_excel(pdf_path: str, output_path: str):
    """Convert PDF tables to Excel for Tableau."""
    df = extract_tables_from_pdf(pdf_path)
    
    if not df.empty:
        # Clean data
        df = df.dropna(how='all')  # Remove empty rows
        df = df.dropna(axis=1, how='all')  # Remove empty columns
        
        # Save to Excel
        df.to_excel(output_path, index=False)
        return True
    return False
```

### PDF Best Practices

- Use `pdfplumber` for table extraction
- Use `pypdf` for basic operations (merge, split)
- Handle multi-page PDFs properly
- Clean extracted data before Tableau import
- Validate data types after extraction

## Project Organization

- Organize workbooks by purpose
- Use consistent naming conventions
- Document data sources
- Maintain version control
- Share best practices
- **Prepare Excel data with formulas, not hardcoded values**
- **Extract PDF tables for Tableau import when needed**
