"""
Basic unit tests for EmailValidator SDK
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from mailsafepro.client import EmailValidator, ValidationResult, BatchResult
from mailsafepro.exceptions import (
    AuthenticationError,
    ValidationError,
    RateLimitError,
)


class TestEmailValidator(unittest.TestCase):
    """Test EmailValidator client"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.api_key = "test_key_12345678901234567890"
        self.base_url = "https://api.test.com"
        self.validator = EmailValidator(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=10,
        )
    
    def test_client_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.validator.base_url, self.base_url)
        self.assertEqual(self.validator._api_key, self.api_key)
        self.assertIsNone(self.validator._access_token)
    
    @patch("requests.Session.request")
    def test_validate_success(self, mock_request):
        """Test successful email validation"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "test@example.com",
            "valid": True,
            "detail": "Valid email",
            "processingtime": 0.123,
            "riskscore": 0.1,
            "qualityscore": 0.9,
            "validationtier": "basic",
            "suggestedaction": "accept",
            "status": "deliverable",
            "provideranalysis": {
                "provider": "gmail",
                "reputation": 0.95,
            },
            "smtpvalidation": {
                "checked": False,
            },
        }
        mock_request.return_value = mock_response
        
        # Test
        result = self.validator.validate("test@example.com")
        
        # Assertions
        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(result.email, "test@example.com")
        self.assertTrue(result.valid)
        self.assertEqual(result.suggested_action, "accept")
    
    @patch("requests.Session.request")
    def test_validate_rate_limit(self, mock_request):
        """Test rate limit handling"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_request.return_value = mock_response
        
        with self.assertRaises(RateLimitError) as context:
            self.validator.validate("test@example.com")
        
        self.assertEqual(context.exception.retry_after, 60)
    
    @patch("requests.Session.request")
    def test_validate_authentication_error(self, mock_request):
        """Test authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Invalid API Key"}
        mock_request.return_value = mock_response
        
        with self.assertRaises(AuthenticationError):
            self.validator.validate("test@example.com")
    
    def test_validate_invalid_email_format(self):
        """Test validation with invalid email format"""
        with self.assertRaises(ValidationError):
            self.validator.validate("invalid-email")
    
    @patch("requests.Session.request")
    def test_validate_batch(self, mock_request):
        """Test batch validation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 2,
            "validcount": 1,
            "invalidcount": 1,
            "processingtime": 0.5,
            "averagetime": 0.25,
            "results": [
                {
                    "email": "valid@example.com",
                    "valid": True,
                    "detail": "Valid",
                    "processingtime": 0.2,
                    "riskscore": 0.1,
                    "qualityscore": 0.9,
                    "validationtier": "basic",
                    "suggestedaction": "accept",
                    "status": "deliverable",
                    "provideranalysis": {"provider": "gmail", "reputation": 0.9},
                    "smtpvalidation": {"checked": False},
                },
                {
                    "email": "invalid@example.com",
                    "valid": False,
                    "detail": "Invalid domain",
                    "processingtime": 0.1,
                    "riskscore": 0.9,
                    "qualityscore": 0.1,
                    "validationtier": "basic",
                    "suggestedaction": "reject",
                    "status": "undeliverable",
                    "provideranalysis": {"provider": "unknown", "reputation": 0.1},
                    "smtpvalidation": {"checked": False},
                },
            ],
        }
        mock_request.return_value = mock_response
        
        result = self.validator.validate_batch(
            ["valid@example.com", "invalid@example.com"]
        )
        
        self.assertIsInstance(result, BatchResult)
        self.assertEqual(result.count, 2)
        self.assertEqual(result.valid_count, 1)
        self.assertEqual(len(result.results), 2)
    
    @patch("requests.Session.post")
    def test_login_success(self, mock_post):
        """Test JWT login"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "access_token_xxx",
            "refresh_token": "refresh_token_xxx",
            "expires_in": 900,
        }
        mock_post.return_value = mock_response
        
        validator = EmailValidator.login(
            username="user@example.com",
            password="password",
            base_url=self.base_url,
        )
        
        self.assertIsNotNone(validator._access_token)
        self.assertIsNotNone(validator._refresh_token)
        self.assertEqual(validator._access_token, "access_token_xxx")


if __name__ == "__main__":
    unittest.main()
