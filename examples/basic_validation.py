#!/usr/bin/env python3
"""
Basic Email Validation Example
================================
Demonstrates simple email validation with MailSafePro SDK.
"""

from mailsafepro import MailSafePro
from mailsafepro.exceptions import (
    EmailValidatorError,
    AuthenticationError,
    ValidationError,
)


def main():
    # Initialize client with API key
    # Replace with your actual API key
    api_key = "key_your_api_key_here"
    
    try:
        client = MailSafePro(api_key=api_key)
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
            
            result = client.validate_email(email)
            
            # Basic information
            print(f"  Email:           {result.email}")
            print(f"  Valid:           {result.is_valid}")
            print(f"  Deliverable:     {result.deliverable}")
            print(f"  Format Valid:    {result.format_valid}")
            print(f"  DNS Valid:       {result.dns_valid}")
            print(f"  Disposable:      {result.is_disposable}")
            print(f"  Free Provider:   {result.is_free_email}")
            print(f"  Role Email:      {result.is_role_email}")
            
            # Risk assessment
            if hasattr(result, 'risk_score'):
                print(f"\n  Risk Score:      {result.risk_score}")
                print(f"  Quality Score:   {result.quality_score}")
            
            # Provider info
            if result.provider_analysis:
                print(f"\n  Provider:        {result.provider_analysis.provider}")
                print(f"  Is Popular:      {result.provider_analysis.is_popular}")
            
            # Security checks
            if result.security_info:
                if result.security_info.spam_trap and result.security_info.spam_trap.checked:
                    print(f"\n  Spam Trap:       {result.security_info.spam_trap.is_spam_trap}")
                    print(f"  Confidence:      {result.security_info.spam_trap.confidence}")
                
                if result.security_info.role_email:
                    print(f"\n  Role Type:       {result.security_info.role_email.role_type}")
            
            # Suggested action
            if hasattr(result, 'suggested_action'):
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
