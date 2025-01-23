# Contributing to AmzPy

Thank you for your interest in contributing to AmzPy! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/theonlyanil/amzpy.git
```

3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Add docstrings for all public functions and classes
- Keep code modular and maintainable

## Adding New Features

1. Create a new branch for your feature:

```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Run tests locally:

```bash
pytest
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the requirements.txt if you add new dependencies
3. Create a Pull Request with a clear description of the changes
4. Wait for review and address any feedback

## Feature Suggestions

- Add support for more product details (ratings, reviews, etc.)
- Implement async support
- Add proxy support
- Create CLI interface
- Add support for product variants
- Implement caching mechanism

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS information

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help maintain a positive community