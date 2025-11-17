#!/usr/bin/env python3
"""
JWT Authentication Example
============================
Demonstrates JWT login and token management with MailSafePro SDK.

Setup:
    1. Copy .env.example to .env
    2. Add your username and password to .env
    3. Run: python examples/jwt_authentication.py
"""

import os
import time
from datetime import datetime
from mailsafepro import MailSafePro
from mailsafepro.exceptions import (
    AuthenticationError,
    EmailValidatorError,
)


def example_jwt_login():
    """Example: Basic JWT authentication"""
    print("=" * 70)
    print("JWT AUTHENTICATION - BASIC LOGIN")
    print("=" * 70 + "\n")

    # Load credentials from environment
    username = os.getenv("MAILSAFEPRO_USERNAME")
    password = os.getenv("MAILSAFEPRO_PASSWORD")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    if not username or not password:
        print("❌ Error: Please set MAILSAFEPRO_USERNAME and MAILSAFEPRO_PASSWORD")
        print("   Copy .env.example to .env and add your credentials")
        return

    try:
        # Login with credentials
        print(f"Logging in as: {username}")
        client = MailSafePro.login(username=username, password=password, base_url=base_url)
        print("✓ Login successful!\n")

        # Validate email
        result = client.validate("test@example.com")
        print(f"Validated: {result.email} - Valid: {result.valid}\n")

        # Logout when done
        client.logout()
        print("✓ Logged out successfully")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
    except EmailValidatorError as e:
        print(f"❌ Error: {e}")


def example_jwt_auto_refresh():
    """Example: JWT token auto-refresh"""
    print("\n" + "=" * 70)
    print("JWT AUTHENTICATION - AUTO REFRESH")
    print("=" * 70 + "\n")

    username = os.getenv("MAILSAFEPRO_USERNAME")
    password = os.getenv("MAILSAFEPRO_PASSWORD")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    if not username or not password:
        print("❌ Error: Credentials not set in environment")
        return

    try:
        # Login
        client = MailSafePro.login(username=username, password=password, base_url=base_url)
        print("✓ Initial login successful\n")

        # Get token expiration info
        if client._access_token:
            print(f"Access Token: {client._access_token[:20]}...")
            if client._token_expires_at:
                expires_in = (client._token_expires_at - datetime.now()).total_seconds()
                print(f"Token expires in: {expires_in / 60:.1f} minutes\n")

        # Simulate long-running process
        print("Simulating long-running validation process...\n")

        for i in range(3):
            # Validate email (token auto-refreshes if needed)
            result = client.validate(f"user{i}@example.com")
            print(f"  [{i+1}] Validated: {result.email} - Valid: {result.valid}")

            # Check if token was refreshed
            if client._access_token:
                print(f"      Token status: Active")

            # Wait a bit
            time.sleep(1)

        print("\n✓ All validations completed with auto-refresh\n")

        # Logout
        client.logout()
        print("✓ Logged out")

    except AuthenticationError as e:
        print(f"❌ Authentication error: {e}")
    except EmailValidatorError as e:
        print(f"❌ Error: {e}")


def example_jwt_with_context_manager():
    """Example: JWT authentication with proper cleanup"""
    print("\n" + "=" * 70)
    print("JWT AUTHENTICATION - WITH CLEANUP")
    print("=" * 70 + "\n")

    username = os.getenv("MAILSAFEPRO_USERNAME")
    password = os.getenv("MAILSAFEPRO_PASSWORD")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    if not username or not password:
        print("❌ Error: Credentials not set in environment")
        return

    try:
        client = MailSafePro.login(username=username, password=password, base_url=base_url)

        try:
            print("✓ Session active\n")

            # Validate multiple emails
            emails = [
                "user1@gmail.com",
                "admin@company.com",
                "test@disposable.com",
            ]

            for email in emails:
                result = client.validate(email)
                status = "✓" if result.valid else "✗"
                print(f"  {status} {email:30} Valid: {result.valid}")

            print()

        finally:
            # Ensure logout even if error occurs
            client.logout()
            print("✓ Session closed (logged out)")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
    except EmailValidatorError as e:
        print(f"❌ Error: {e}")


def example_session_info():
    """Example: Get session information"""
    print("\n" + "=" * 70)
    print("JWT AUTHENTICATION - SESSION INFO")
    print("=" * 70 + "\n")

    username = os.getenv("MAILSAFEPRO_USERNAME")
    password = os.getenv("MAILSAFEPRO_PASSWORD")
    base_url = os.getenv("MAILSAFEPRO_BASE_URL", "https://api.mailsafepro.com")

    if not username or not password:
        print("❌ Error: Credentials not set in environment")
        return

    try:
        client = MailSafePro.login(username=username, password=password, base_url=base_url)
        print("✓ Login successful\n")

        # Display session information
        print("Session Information:")
        print("-" * 70)

        if client._access_token:
            print(f"  Token (first 30 chars): {client._access_token[:30]}...")

        if client._token_expires_at:
            expires_in = (client._token_expires_at - datetime.now()).total_seconds()
            print(f"  Token expires in:       {expires_in / 60:.1f} minutes")
            print(f"  Token expires at:       {client._token_expires_at.strftime('%Y-%m-%d %H:%M:%S')}")

        if client._refresh_token:
            print(f"  Refresh token:          Available")

        print("-" * 70)

        # Logout
        client.logout()
        print("\n✓ Logged out")

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")


def main():
    """Run all JWT authentication examples"""
    print("\n")
    print("#" * 70)
    print("#  MailSafePro SDK - JWT Authentication Examples")
    print("#" * 70)
    print("\nSetup: Copy .env.example to .env and add your credentials\n")

    # Run examples
    example_jwt_login()
    example_jwt_auto_refresh()
    example_jwt_with_context_manager()
    example_session_info()

    print("\n" + "#" * 70)
    print("All examples completed!")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    main()
