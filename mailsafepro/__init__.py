"""
MailSafePro SDK - Official Python client for Email Validation API
"""

__version__ = "2.0.0"
__author__ = "MailSafePro Team"
__license__ = "MIT"

from .client import MailSafePro, AsyncMailSafePro, ClientConfig
from .models import (
    ValidationResult,
    BatchResult,
    UsageStats,
    SMTPInfo,
    DNSInfo,
    DNSRecordSPF,
    DNSRecordDKIM,
    DNSRecordDMARC,
    ProviderAnalysis,
    SecurityInfo,
    SpamTrapCheck,
    RoleEmailInfo,
    BreachInfo,
    SuggestedFixes,
    Metadata,
)
from .exceptions import (
    EmailValidatorError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    QuotaExceededError,
    ServerError,
    NetworkError,
)

__all__ = [
    "MailSafePro",
    "AsyncMailSafePro",
    "ClientConfig",
    "ValidationResult",
    "BatchResult",
    "UsageStats",
    "SMTPInfo",
    "DNSInfo",
    "DNSRecordSPF",
    "DNSRecordDKIM",
    "DNSRecordDMARC",
    "ProviderAnalysis",
    "SecurityInfo",
    "SpamTrapCheck",
    "RoleEmailInfo",
    "BreachInfo",
    "SuggestedFixes",
    "Metadata",
    "EmailValidatorError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "QuotaExceededError",
    "ServerError",
    "NetworkError",
]
