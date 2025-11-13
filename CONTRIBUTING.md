# Contributing to MailSafePro SDK

Thank you for your interest in contributing to the MailSafePro Python SDK! 🎉

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Poetry (for dependency management)
- Git

### Setup Steps

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/mailsafepro-python-sdk.git
cd mailsafepro-python-sdk
```

2. **Install dependencies**

```bash
poetry install
```

3. **Run tests**

```bash
poetry run pytest tests/ -v
```

## Making Changes

### Branch Naming Convention
- Feature: `feature/your-feature-name`
- Bug fix: `fix/your-bug-fix`
- Documentation: `docs/your-documentation-update`

### Commit Message Format
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

**Examples:**

```bash
git commit -m "feat: add email disposable domain check"
git commit -m "fix: resolve JWT token refresh issue"
git commit -m "docs: update installation guide"
```

## Pull Request Process

1. **Fork the repository** on GitHub
2. **Create a feature branch**

```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
- Write clear, concise code
- Add tests for new functionality
- Update documentation as needed
4. **Run tests and ensure they pass**

```bash
poetry run pytest tests/ -v
```

5. **Commit your changes**

```bash
git add .
git commit -m "feat: add amazing feature"
```

6. **Push to your fork**

```bash
git push origin feature/amazing-feature
```

7. **Open a Pull Request** on the original repository

## Code Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small (single responsibility)
- Use meaningful variable and function names

### Running Code Formatters

Format code with Black

```bash
poetry run black mailsafepro/
```

Type checking with mypy

```bash
poetry run mypy mailsafepro/ --ignore-missing-imports
```

## Testing Requirements

- Write tests for all new features
- Ensure existing tests pass before submitting PR
- Aim for high code coverage (>80%)
- Test edge cases and error conditions

### Running Tests

Run all tests

```bash
poetry run pytest tests/ -v
```

Run with coverage report

```bash
poetry run pytest tests/ -v --cov=mailsafepro --cov-report=term-missing
```

Run specific test file

```bash
poetry run pytest tests/test_client.py -v
```

## Reporting Issues

When reporting bugs, please include:
- Python version
- SDK version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or stack traces

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Explain the use case
- Describe the expected behavior
- Consider if it fits the project scope

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Discussions about improvements

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to make this project better!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MailSafePro! 🚀