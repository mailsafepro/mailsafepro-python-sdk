# Changelog

All notable changes to the MailSafePro Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-03

### Security Improvements
- **SecureString class**: API keys and tokens are now wrapped in SecureString to prevent accidental logging
- **Memory protection**: Tokens are overwritten on deletion to prevent memory inspection attacks
- **Sensitive data masking**: All logs automatically mask emails, API keys, passwords, and JWT tokens
- **Request ID tracking**: Every request gets a unique ID for debugging and support tracking
- **Credential validation**: Login now validates credentials before making requests

### New Features
- **Rate limiting awareness**: Client tracks rate limit headers and warns before hitting limits
- **Request counting**: Track total requests made with `client.request_count`
- **Rate limit property**: Check remaining quota with `client.rate_limit_remaining`
- **ConfigurationError exception**: New exception for invalid SDK configuration
- **Proxy support**: Added `proxy` option to ClientConfig
- **SSL verification toggle**: Added `verify_ssl` option for development environments
- **Token jitter**: Automatic jitter added to token refresh to prevent thundering herd

### Improvements
- **Better error messages**: All exceptions now include request_id and detailed context
- **Exception serialization**: Added `to_dict()` method to all exceptions for logging
- **Deprecation warnings**: `get_quota()` now uses proper Python warnings
- **Dynamic timeout**: Batch validation timeout scales with email count
- **Thread-safe token refresh**: Token refresh is now protected by threading lock
- **Async lock support**: AsyncMailSafePro uses asyncio.Lock for token refresh

### API Changes
- Updated endpoints to use `/v1/` prefix for versioning
- Added `X-SDK-Version` header to all requests
- Added `X-Request-ID` header for request tracking

### Bug Fixes
- Fixed inconsistency between tests (using requests) and client (using httpx)
- Fixed missing `logout()` method implementation
- Fixed potential race condition in token refresh
- Fixed file validation allowing files larger than 10MB

### Developer Experience
- Added `py.typed` marker for PEP 561 compliance
- Updated type hints throughout codebase
- Added `ruff` for linting alongside `black`
- Added `respx` for httpx mocking in tests
- Improved test coverage with new test cases

### Dependencies
- Removed `requests` dependency (was unused)
- Added optional `aiofiles` for async file operations
- Updated minimum `httpx` version to 0.24.0
- Updated minimum `pydantic` version to 2.0.0

## [2.0.0] - 2024-12-15

### Breaking Changes
- Migrated from `requests` to `httpx` for HTTP client
- Updated to Pydantic v2 for data validation
- Changed model field names to use snake_case consistently

### New Features
- Added `AsyncMailSafePro` client for async/await support
- Added `ClientConfig` dataclass for configuration
- Added context manager support (`with` statement)
- Added JWT authentication with auto-refresh
- Added batch validation with auto-chunking for large lists
- Added file upload validation (CSV/TXT)

### Improvements
- Full type hints for IDE autocompletion
- Automatic retry with exponential backoff
- Better error handling with specific exception types
- Comprehensive validation result models

## [1.0.2] - 2024-11-01

### Fixed
- Fixed email format validation regex
- Fixed batch validation response parsing

## [1.0.1] - 2024-10-15

### Fixed
- Fixed authentication header format
- Fixed timeout handling

## [1.0.0] - 2024-10-01

### Initial Release
- Basic email validation
- API key authentication
- Simple error handling
