# MailSafePro SDK Examples

This directory contains practical examples demonstrating how to use the MailSafePro Python SDK.

## 📋 Prerequisites

Install the SDK

```bash
pip install mailsafepro-sdk
```

Or from the repository root
```bash
pip install -e .
```

## 🚀 Running the Examples

### 1. Basic Validation (`basic_validation.py`)

Demonstrates simple email validation with detailed output.

Edit the file and replace 'key_your_api_key_here' with your actual API key

```bash
python examples/basic_validation.py
```

**Features demonstrated:**
- Single email validation
- Format, DNS, and deliverability checks
- Disposable and role email detection
- Provider analysis
- Security checks (spam trap, breach info)
- Risk scoring

### 2. Batch Processing (`batch_processing.py`)

Shows how to validate multiple emails efficiently.

Edit the file and replace 'key_your_api_key_here' with your actual API key

```bash
python examples/batch_processing.py
```

**Features demonstrated:**
- Batch email validation
- Performance timing
- Results grouping (valid, invalid, risky)
- Statistics and reporting
- File upload validation (CSV/TXT)

### 3. JWT Authentication (`jwt_authentication.py`)

Demonstrates JWT login and token management.

Edit the file and replace credentials with your actual username/password

```bash
python examples/jwt_authentication.py
```

**Features demonstrated:**
- JWT login/logout
- Automatic token refresh
- Session management
- Context manager pattern
- Token expiration handling

## 📁 File Structure

examples/
├── README.md # This file
├── basic_validation.py # Basic validation example
├── batch_processing.py # Batch processing example
└── jwt_authentication.py # JWT authentication example


## 🔑 API Keys

To run these examples, you need:

1. **API Key** (for basic_validation.py and batch_processing.py)
   - Get from: https://mailsafepro.com/dashboard/api-keys

2. **Account Credentials** (for jwt_authentication.py)
   - Username (email) and password from your MailSafePro account

## 💡 Tips

- Start with `basic_validation.py` to understand the basics
- Use `batch_processing.py` for validating large lists
- Use `jwt_authentication.py` when you need dynamic authentication
- Replace placeholder credentials before running
- Check error handling in each example for production use patterns

## 📚 Additional Resources

- **Documentation:** https://docs.mailsafepro.com/sdk/python
- **API Reference:** https://docs.mailsafepro.com/api
- **GitHub:** https://github.com/mailsafepro/mailsafepro-python-sdk
- **Support:** support@mailsafepro.com

## 🐛 Issues

If you encounter any issues with these examples, please open an issue on GitHub:
https://github.com/mailsafepro/mailsafepro-python-sdk/issues