# Contributing to TermChat 🤝

First of all, thank you for your interest in contributing to TermChat! Your contributions help make this project better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Reporting](#issue-reporting)

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We welcome contributions from everyone regardless of experience level.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment (see below)
4. Make your changes
5. Submit a Pull Request

## 🛠 Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/termchat.git
cd termchat

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/
```

## 📝 How to Contribute

### Reporting Bugs
- Use GitHub Issues with a clear description
- Include steps to reproduce, expected behavior, and actual behavior
- Specify your OS, Python version, and TermChat version

### Suggesting Features
- Open an Issue with the `[Feature]` tag
- Describe the use case and expected behavior

### Code Contributions
1. Create a branch from `main`: `git checkout -b feature/your-feature`
2. Write code with clear comments
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Run linter: `ruff check src/`
6. Commit with conventional commit messages:
   - `feat: add new feature`
   - `fix: resolve bug`
   - `docs: update documentation`
   - `refactor: code restructuring`
   - `test: add/update tests`

## 📤 Pull Request Guidelines

- Keep PRs focused on a single concern
- Include a clear description of changes
- Ensure all tests pass
- Update documentation if needed
- Be responsive to review feedback

## 🐛 Issue Reporting

When reporting issues, please include:
- **OS**: (e.g., Ubuntu 22.04, macOS 14, Windows 11)
- **Python version**: (e.g., 3.11.5)
- **TermChat version**: (e.g., 1.0.0)
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error logs** (if applicable)

Thank you for contributing! 🎉
