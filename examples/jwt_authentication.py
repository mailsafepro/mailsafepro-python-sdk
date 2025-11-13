#!/usr/bin/env python3
"""
JWT Authentication Example
============================
Demonstrates JWT login and token management with MailSafePro SDK.
"""

import time
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
    
    # Login credentials
    username = "your_email@example.com"
    password = "your_password"
    
    try:
        # Login with credentials
        print(f"Logging in as: {username}")
        client = MailSafePro.login(username=username, password=password)
        print("✓ Login successful!\n")
        
        # Validate email
        result = client.validate_email("test@example.com")
        print(f"Validated: {result.email} - Valid: {result.is_valid}\n")
        
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
    
    username = "your_email@example.com"
    password = "your_password"
    
    try:
        # Login
        client = MailSafePro.login(username=username, password=password)
        print("✓ Initial login successful\n")
        
        # Get token expiration info
        if hasattr(client, '_jwt_token'):
            print(f"JWT Token: {client._jwt_token[:20]}...")
            if hasattr(client, '_jwt_expires_at'):
                expires_in = client._jwt_expires_at - time.time()
                print(f"Token expires in: {expires_in / 60:.1f} minutes\n")
        
        # Simulate long-running process
        print("Simulating long-running validation process...\n")
        
        for i in range(3):
            # Validate email (token auto-refreshes if needed)
            result = client.validate_email(f"user{i}@example.com")
            print(f"  [{i+1}] Validated: {result.email} - Valid: {result.is_valid}")
            
            # Check if token was refreshed
            if hasattr(client, '_jwt_token'):
                print(f"      Token status: Active")
            
            # Wait a bit (in real scenario, this could be minutes)
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
    """Example: JWT authentication with context manager"""
    print("\n" + "=" * 70)
    print("JWT AUTHENTICATION - CONTEXT MANAGER")
    print("=" * 70 + "\n")
    
    username = "your_email@example.com"
    password = "your_password"
    
    # Note: This is conceptual - actual SDK may not support context manager
    # but demonstrates good practice
    try:
        client = MailSafePro.login(username=username, password=password)
        
        try:
            print("✓ Session active\n")
            
            # Validate multiple emails
            emails = [
                "user1@gmail.com",
                "admin@company.com",
                "test@disposable.com",
            ]
            
            for email in emails:
                result = client.validate_email(email)
                status = "✓" if result.is_valid else "✗"
                print(f"  {status} {email:30} Valid: {result.is_valid}")
            
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
    
    username = "your_email@example.com"
    password = "your_password"
    
    try:
        client = MailSafePro.login(username=username, password=password)
        print("✓ Login successful\n")
        
        # Display session information
        print("Session Information:")
        print("-" * 70)
        
        if hasattr(client, '_jwt_token'):
            print(f"  Token (first 30 chars): {client._jwt_token[:30]}...")
        
        if hasattr(client, '_jwt_expires_at'):
            expires_at = client._jwt_expires_at
            expires_in = expires_at - time.time()
            print(f"  Token expires in:       {expires_in / 60:.1f} minutes")
            print(f"  Token expires at:       {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expires_at))}")
        
        if hasattr(client, '_refresh_token'):
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
    print("\nNote: Replace credentials with your actual username and password\n")
    
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
