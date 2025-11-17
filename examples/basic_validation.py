#!/usr/bin/env python3
"""
Basic Email Validation Example
================================
Demonstrates simple email validation with MailSafePro SDK.

Setup:
    1. Copy .env.example to .env
    2. Add your API key to .env
    3. Run: python examples/basic_validation.py
"""

import os
from mailsafepro import MailSafePro
from mailsafepro.exceptions import (
    EmailValidatorError,
    AuthenticationError,
    ValidationError,
)


def main():
    # Load configuration from environment variables
    api_key = os.getenv("MAILSAFEPRO_API_KEY")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    # Validate API key is provided
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ Error: Please set MAILSAFEPRO_API_KEY environment variable")
        print("   Copy .env.example to .env and add your API key")
        return

    try:
        client = MailSafePro(api_key=api_key, base_url=base_url)
        print("✓ Client initialized successfully\n")
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return

    # List of emails to validate
    test_emails = [
        "user@gmail.com",
        "admin@example.com",
        "invalid@",
        "test@disposable-email.com",
        "contact@company.co.uk",
    ]

    print("=" * 70)
    print("BASIC EMAIL VALIDATION")
    print("=" * 70 + "\n")

    # Validate each email
    for email in test_emails:
        try:
            print(f"Validating: {email}")
            print("-" * 70)

            result = client.validate(email)

            # Basic information
            print(f"  Email:           {result.email}")
            print(f"  Valid:           {result.valid}")
            print(f"  Status:          {result.status}")
            print(f"  Detail:          {result.detail}")
            print(f"  Processing Time: {result.processing_time:.3f}s")

            # Risk assessment
            print(f"\n  Risk Score:      {result.risk_score:.2f}")
            print(f"  Quality Score:   {result.quality_score:.2f}")

            # Provider info
            if result.provider_analysis:
                print(f"\n  Provider:        {result.provider_analysis.provider}")
                print(f"  Reputation:      {result.provider_analysis.reputation:.2f}")

            # SMTP info
            if result.smtp and result.smtp.checked:
                print(f"\n  SMTP Checked:    {result.smtp.checked}")
                print(f"  Mailbox Exists:  {result.smtp.mailbox_exists}")

            # DNS info
            if result.dns_security:
                print(f"\n  MX Records:      {len(result.dns_security.mx_records)}")
                if result.dns_security.spf:
                    print(f"  SPF Status:      {result.dns_security.spf.status}")
                if result.dns_security.dmarc:
                    print(f"  DMARC Policy:    {result.dns_security.dmarc.policy}")

            # Spam trap check
            if result.spam_trap_check and result.spam_trap_check.checked:
                print(f"\n  Spam Trap:       {result.spam_trap_check.is_spam_trap}")
                print(f"  Confidence:      {result.spam_trap_check.confidence:.2f}")

            # Role email info
            if result.role_email_info:
                print(f"\n  Role Email:      {result.role_email_info.is_role_email}")
                if result.role_email_info.is_role_email:
                    print(f"  Role Type:       {result.role_email_info.role_type}")

            # Breach info
            if result.breach_info:
                print(f"\n  In Breach:       {result.breach_info.in_breach}")
                if result.breach_info.in_breach:
                    print(f"  Breach Count:    {result.breach_info.breach_count}")

            # Suggested fixes
            if result.suggested_fixes and result.suggested_fixes.typo_detected:
                print(f"\n  Typo Detected:   {result.suggested_fixes.typo_detected}")
                print(f"  Suggested:       {result.suggested_fixes.suggested_email}")

            # Suggested action
            print(f"\n  ⚡ Suggested Action: {result.suggested_action.upper()}")

            print()

        except ValidationError as e:
            print(f"  ❌ Validation error: {e}\n")
        except EmailValidatorError as e:
            print(f"  ❌ Error: {e}\n")

    print("=" * 70)
    print("Validation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
