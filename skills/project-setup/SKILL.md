---
name: project-setup
description: Sets up new projects with proper structure, dependencies, and configuration. Creates project scaffolding, initializes version control, and configures development environment. Use when starting a new project, setting up project structure, or initializing development environment.
---

# Project Setup

## Quick Start

When setting up a new project:

1. Define project structure
2. Initialize version control
3. Set up dependencies
4. Configure development tools
5. Create initial documentation

## Project Structure

### Python Projects

```
project-name/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── docs/
└── scripts/
```

### Data Analysis Projects

```
project-name/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
├── notebooks/
├── src/
│   └── analysis.py
└── reports/
```

## Initialization Steps

### 1. Version Control

- Initialize git repository
- Create `.gitignore` appropriate for project type
- Set up initial commit
- Configure remote repository if needed

### 2. Dependencies

- Create `requirements.txt` (Python)
- Document package versions
- Include development dependencies
- Set up virtual environment

### 3. Configuration

- Create `.env.example` for environment variables
- Set up configuration files
- Document configuration options
- Add to `.gitignore` if sensitive

### 4. Documentation

- Write clear README.md
- Document setup instructions
- Include usage examples
- Add contribution guidelines

## Python Setup

### Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Project Structure

- Use `src/` layout for packages
- Separate tests from source code
- Organize by feature/domain
- Keep entry points clear

## Best Practices

### .gitignore

Include:
- Virtual environments (`venv/`, `.venv/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Environment files (`.env`)
- Build artifacts (`__pycache__/`, `*.pyc`)

### README.md

Include:
- Project description
- Installation instructions
- Usage examples
- Configuration guide
- Contributing guidelines

### Code Quality

- Set up linters (flake8, pylint)
- Configure formatters (black, autopep8)
- Add pre-commit hooks
- Set up CI/CD basics

## Common Configurations

### Python Project

- `setup.py` or `pyproject.toml` for packages
- `requirements.txt` for dependencies
- `.pylintrc` or `pyproject.toml` for linting
- `pytest.ini` for testing

### Data Project

- Jupyter notebook configuration
- Data pipeline structure
- Output directory organization
- Documentation standards
