#!/usr/bin/env python3
"""
Batch Email Validation Example
================================
Demonstrates batch processing with MailSafePro SDK.

Setup:
    1. Copy .env.example to .env
    2. Add your API key to .env
    3. Run: python examples/batch_processing.py
"""

import os
import time
from mailsafepro import MailSafePro
from mailsafepro.exceptions import (
    EmailValidatorError,
    RateLimitError,
    QuotaExceededError,
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

    # Initialize client
    client = MailSafePro(api_key=api_key, base_url=base_url, timeout=60)

    print("=" * 70)
    print("BATCH EMAIL VALIDATION")
    print("=" * 70 + "\n")

    # Large batch of emails to validate
    email_batch = [
        "user1@gmail.com",
        "user2@yahoo.com",
        "admin@example.com",
        "sales@company.com",
        "contact@startup.io",
        "info@business.co.uk",
        "support@saas-product.com",
        "hello@freelancer.dev",
    ]

    print(f"📧 Validating {len(email_batch)} emails...\n")

    try:
        # Start timing
        start_time = time.time()

        # Validate batch
        batch_result = client.validate_batch(email_batch)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        print("✓ Batch validation complete!\n")
        print("=" * 70)
        print("BATCH SUMMARY")
        print("=" * 70)
        print(f"  Total Emails:      {batch_result.count}")
        print(f"  Valid:             {batch_result.valid_count}")
        print(f"  Invalid:           {batch_result.invalid_count}")
        print(f"  Processing Time:   {batch_result.processing_time:.2f}s")
        print(f"  Avg per email:     {batch_result.average_time:.3f}s")
        print("=" * 70 + "\n")

        # Detailed results
        print("=" * 70)
        print("DETAILED RESULTS")
        print("=" * 70 + "\n")

        # Group by status
        valid_emails = []
        invalid_emails = []
        risky_emails = []

        for result in batch_result.results:
            if result.valid and result.status == "deliverable":
                valid_emails.append(result)
            elif not result.valid:
                invalid_emails.append(result)
            else:
                risky_emails.append(result)

        # Display valid emails
        if valid_emails:
            print("✅ VALID EMAILS:")
            for result in valid_emails:
                provider = result.provider_analysis.provider if result.provider_analysis else "Unknown"
                print(f"  • {result.email:35} [{provider}] - Risk: {result.risk_score:.2f}")
            print()

        # Display risky emails
        if risky_emails:
            print("⚠️  RISKY EMAILS:")
            for result in risky_emails:
                reasons = []
                if result.role_email_info and result.role_email_info.is_role_email:
                    reasons.append("Role Email")
                if result.spam_trap_check and result.spam_trap_check.is_spam_trap:
                    reasons.append("Spam Trap")
                if result.breach_info and result.breach_info.in_breach:
                    reasons.append("Data Breach")
                if result.risk_score > 0.7:
                    reasons.append("High Risk")

                reason_str = ", ".join(reasons) if reasons else f"Risk: {result.risk_score:.2f}"
                print(f"  • {result.email:35} [{reason_str}]")
            print()

        # Display invalid emails
        if invalid_emails:
            print("❌ INVALID EMAILS:")
            for result in invalid_emails:
                print(f"  • {result.email:35} [{result.detail}]")
            print()

        # Statistics
        print("=" * 70)
        print("STATISTICS")
        print("=" * 70)

        role_count = sum(1 for r in batch_result.results if r.role_email_info and r.role_email_info.is_role_email)
        spam_trap_count = sum(1 for r in batch_result.results if r.spam_trap_check and r.spam_trap_check.is_spam_trap)
        breach_count = sum(1 for r in batch_result.results if r.breach_info and r.breach_info.in_breach)
        high_risk_count = sum(1 for r in batch_result.results if r.risk_score > 0.7)

        print(f"  Role Emails:       {role_count}")
        print(f"  Spam Traps:        {spam_trap_count}")
        print(f"  Breached Emails:   {breach_count}")
        print(f"  High Risk:         {high_risk_count}")
        print("=" * 70)

    except RateLimitError as e:
        print(f"❌ Rate limit exceeded. Retry after {e.retry_after} seconds")
    except QuotaExceededError as e:
        print(f"❌ Daily quota exceeded: {e}")
    except EmailValidatorError as e:
        print(f"❌ Error during batch validation: {e}")


def validate_from_file():
    """Example: Validate emails from a CSV file"""
    api_key = os.getenv("MAILSAFEPRO_API_KEY")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ Error: Please set MAILSAFEPRO_API_KEY environment variable")
        return

    client = MailSafePro(api_key=api_key, base_url=base_url)

    # Assuming you have a CSV file with emails
    csv_file = "emails.csv"

    print(f"\n📁 Validating emails from file: {csv_file}\n")

    try:
        result = client.validate_file(
            file_path=csv_file, column="email", check_smtp=False  # Column name containing emails
        )

        print(f"✓ Processed {result.count} emails from file")
        print(f"  Valid: {result.valid_count}")
        print(f"  Invalid: {result.invalid_count}")

    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
    except EmailValidatorError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

    # Uncomment to test file validation
    # validate_from_file()
