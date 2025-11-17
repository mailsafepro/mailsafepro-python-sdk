# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🛡️ Reporting a Vulnerability

We take the security of MailSafePro SDK seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

**Please DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, report security issues privately to:

📧 **Email:** security@mailsafepro.com

Include the following information in your report:

- **Type of vulnerability** (e.g., authentication bypass, SQL injection, XSS, etc.)
- **Full path of source file(s)** related to the vulnerability
- **Location of affected code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability** (what an attacker could achieve)
- **Any suggested fixes** (optional)

### What to Expect

After submitting a vulnerability report, you can expect:

1. **Acknowledgment:** We will acknowledge receipt of your report within **48 hours**
2. **Assessment:** We will investigate and assess the severity within **5 business days**
3. **Updates:** We will provide status updates at least every **7 days**
4. **Resolution Timeline:**
   - **Critical:** Fix within 7 days
   - **High:** Fix within 14 days
   - **Medium:** Fix within 30 days
   - **Low:** Fix within 90 days

### Disclosure Policy

- Please give us reasonable time to address the vulnerability before making it public
- We follow **Coordinated Vulnerability Disclosure** (CVD) practices
- Once a fix is released, we will publish a security advisory on GitHub
- We will credit you in the advisory (unless you prefer to remain anonymous)

## 🏆 Security Researchers Recognition

We appreciate security researchers who help keep MailSafePro safe. Valid security reports may be eligible for:

- Public acknowledgment in our Security Hall of Fame
- Credit in release notes and security advisories
- Swag and thank-you gifts (for significant findings)

## 🔐 Security Best Practices for Users

### API Key Security

**DO:**
- ✅ Store API keys in environment variables (`.env` files)
- ✅ Use different API keys for development/staging/production
- ✅ Rotate API keys every 90 days
- ✅ Revoke compromised keys immediately
- ✅ Use key management systems (AWS Secrets Manager, Azure Key Vault, etc.)

**DON'T:**
- ❌ Commit API keys to version control
- ❌ Share API keys in public channels (Slack, Discord, forums)
- ❌ Hardcode API keys in source code
- ❌ Use the same API key across multiple environments
- ❌ Store API keys in plain text files

### JWT Authentication Security

**DO:**
- ✅ Store refresh tokens securely (encrypted storage)
- ✅ Implement token rotation
- ✅ Use HTTPS for all API requests
- ✅ Logout when session ends
- ✅ Monitor for unusual authentication patterns

**DON'T:**
- ❌ Store tokens in local storage (browser)
- ❌ Share JWT tokens between users
- ❌ Use weak passwords
- ❌ Disable token expiration

### Network Security

**DO:**
- ✅ Always use HTTPS endpoints in production
- ✅ Validate SSL certificates
- ✅ Use VPN for sensitive operations
- ✅ Monitor API usage for anomalies
- ✅ Implement rate limiting in your application

**DON'T:**
- ❌ Use HTTP in production
- ❌ Disable SSL verification
- ❌ Expose internal endpoints publicly
- ❌ Trust user input without validation

### Code Security

**DO:**
- ✅ Keep the SDK updated to the latest version
- ✅ Review dependency security with `safety check`
- ✅ Run `bandit` for Python security linting
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Implement input validation

**DON'T:**
- ❌ Use outdated SDK versions with known vulnerabilities
- ❌ Ignore security warnings from dependency scanners
- ❌ Commit `.env` files or credentials
- ❌ Trust unvalidated email addresses

## 🚨 Known Security Considerations

### Current Scope

The SDK provides secure communication with the MailSafePro API, but users are responsible for:

- **Credential Management:** Securely storing and rotating API keys/passwords
- **Network Security:** Using HTTPS in production environments
- **Access Control:** Implementing proper authorization in their applications
- **Data Handling:** Protecting validation results containing sensitive information
- **Compliance:** Meeting regulatory requirements (GDPR, CCPA, etc.)

### Out of Scope

The following are **not considered security vulnerabilities**:

- Denial of service attacks against the MailSafePro API (report to API team)
- Social engineering attacks targeting MailSafePro users
- Issues in third-party dependencies (report to the respective project)
- Theoretical vulnerabilities without proof of concept
- Rate limiting or quota issues (these are business logic, not security)

## 🛠️ Security Tools

We use the following tools to maintain security:

- **Bandit:** Python security linter
- **Safety:** Dependency vulnerability scanner
- **GitHub Dependabot:** Automated dependency updates
- **CodeQL:** Static analysis for security vulnerabilities
- **pytest:** Comprehensive test coverage

### Run Security Scans Locally

