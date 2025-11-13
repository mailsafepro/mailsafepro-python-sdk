#!/usr/bin/env python3
"""
Batch Email Validation Example
================================
Demonstrates batch processing with MailSafePro SDK.
"""

import time
from mailsafepro import MailSafePro
from mailsafepro.exceptions import (
    EmailValidatorError,
    RateLimitError,
    QuotaExceededError,
)


def main():
    # Initialize client
    api_key = "key_your_api_key_here"
    client = MailSafePro(api_key=api_key, timeout=60)
    
    print("=" * 70)
    print("BATCH EMAIL VALIDATION")
    print("=" * 70 + "\n")

    # Large batch of emails to validate
    email_batch = [
        "user1@gmail.com",
        "user2@yahoo.com",
        "admin@example.com",
        "sales@company.com",
        "invalid@test",
        "temp@10minutemail.com",
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
        print(f"  Total Emails:      {batch_result.total_count}")
        print(f"  Valid:             {batch_result.valid_count}")
        print(f"  Invalid:           {batch_result.invalid_count}")
        print(f"  Deliverable:       {batch_result.deliverable_count}")
        print(f"  Risky:             {batch_result.risky_count}")
        print(f"  Unknown:           {batch_result.unknown_count}")
        print(f"  Processing Time:   {elapsed_time:.2f}s")
        print(f"  Avg per email:     {elapsed_time / len(email_batch):.3f}s")
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
            if result.is_valid and result.deliverable:
                valid_emails.append(result)
            elif not result.is_valid:
                invalid_emails.append(result)
            else:
                risky_emails.append(result)
        
        # Display valid emails
        if valid_emails:
            print("✅ VALID EMAILS:")
            for result in valid_emails:
                provider = result.provider_analysis.provider if result.provider_analysis else "Unknown"
                print(f"  • {result.email:35} [{provider}]")
            print()
        
        # Display risky emails
        if risky_emails:
            print("⚠️  RISKY EMAILS:")
            for result in risky_emails:
                reasons = []
                if result.is_disposable:
                    reasons.append("Disposable")
                if result.is_role_email:
                    reasons.append("Role Email")
                if result.security_info and result.security_info.spam_trap:
                    if result.security_info.spam_trap.is_spam_trap:
                        reasons.append("Spam Trap")
                
                reason_str = ", ".join(reasons) if reasons else "Low quality"
                print(f"  • {result.email:35} [{reason_str}]")
            print()
        
        # Display invalid emails
        if invalid_emails:
            print("❌ INVALID EMAILS:")
            for result in invalid_emails:
                reason = "Invalid format" if not result.format_valid else "DNS/Domain issue"
                print(f"  • {result.email:35} [{reason}]")
            print()
        
        # Statistics
        print("=" * 70)
        print("STATISTICS")
        print("=" * 70)
        
        # Count disposable emails
        disposable_count = sum(1 for r in batch_result.results if r.is_disposable)
        role_count = sum(1 for r in batch_result.results if r.is_role_email)
        free_count = sum(1 for r in batch_result.results if r.is_free_email)
        
        print(f"  Disposable Emails: {disposable_count}")
        print(f"  Role Emails:       {role_count}")
        print(f"  Free Providers:    {free_count}")
        print("=" * 70)
        
    except RateLimitError as e:
        print(f"❌ Rate limit exceeded. Retry after {e.retry_after} seconds")
    except QuotaExceededError as e:
        print(f"❌ Daily quota exceeded: {e}")
    except EmailValidatorError as e:
        print(f"❌ Error during batch validation: {e}")


def validate_from_file():
    """Example: Validate emails from a CSV file"""
    api_key = "key_your_api_key_here"
    client = MailSafePro(api_key=api_key)
    
    # Assuming you have a CSV file with emails
    csv_file = "emails.csv"
    
    print(f"\n📁 Validating emails from file: {csv_file}\n")
    
    try:
        result = client.validate_file(
            file_path=csv_file,
            column="email",  # Column name containing emails
            check_smtp=False
        )
        
        print(f"✓ Processed {result.total_count} emails from file")
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
