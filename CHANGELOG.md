# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Integration with additional email validation providers
- Webhook support for batch processing
- CLI tool for quick email validation

## [1.0.0] - 2025-11-12

### Added
- Initial release of MailSafePro Python SDK
- **Email Validation:**
  - Format validation (RFC 5322 compliant)
  - DNS record validation (MX, A records)
  - SMTP server verification
  - Disposable email detection
  - Free email provider detection
- **Security Features:**
  - Spam trap detection
  - Breach checking integration (Have I Been Pwned)
  - Role-based email detection (admin@, info@, etc.)
  - Toxic/abuse domain detection
- **DNS Authentication:**
  - SPF record validation
  - DKIM record validation
  - DMARC policy checking
- **Provider Analysis:**
  - Email provider identification
  - Provider-specific recommendations
- **Batch Processing:**
  - Bulk email validation
  - File upload support (CSV, TXT)
  - Asynchronous processing support
- **Authentication:**
  - API Key authentication
  - JWT authentication with auto-refresh
  - Token expiration handling
- **Developer Experience:**
  - Comprehensive error handling with custom exceptions
  - Full type hints support (Python 3.8+)
  - Retry logic with exponential backoff
  - Request/response logging
  - Response caching support
- **Documentation:**
  - Complete API documentation
  - Usage examples for all features
  - Installation guide
  - Troubleshooting guide

### Dependencies
- `requests >= 2.31.0` - HTTP client
- `urllib3 >= 2.0.0` - HTTP library with connection pooling

[Unreleased]: https://github.com/mailsafepro/mailsafepro-python-sdk/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/mailsafepro/mailsafepro-python-sdk/releases/tag/v1.0.0
