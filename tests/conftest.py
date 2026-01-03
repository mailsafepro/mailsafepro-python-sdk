"""
Pytest configuration and shared fixtures
"""
import pytest
from datetime import datetime


@pytest.fixture
def mock_validation_response():
    """Mock successful validation API response"""
    return {
        "email": "test@example.com",
        "valid": True,
        "detail": "Email is valid and deliverable",
        "processing_time": 0.15,
        "risk_score": 0.1,
        "quality_score": 0.95,
        "validation_tier": "standard",
        "suggested_action": "accept",
        "status": "deliverable",
        "provider_analysis": {
            "provider": "Gmail",
            "reputation": 0.95,
            "fingerprint": "google-workspace"
        },
        "smtp": {
            "checked": True,
            "mailbox_exists": True,
            "mx_server": "gmail-smtp-in.l.google.com",
            "response_time": 0.05,
        },
        "dns_security": {
            "spf": {"status": "pass", "record": "v=spf1 include:_spf.google.com ~all"},
            "dkim": {"status": "pass", "selector": "google"},
            "dmarc": {"status": "pass", "policy": "reject"},
            "mx_records": ["gmail-smtp-in.l.google.com"],
            "ns_records": ["ns1.google.com"],
        },
        "spam_trap_check": {
            "checked": True,
            "is_spam_trap": False,
            "confidence": 0.99,
            "trap_type": "none",
            "source": "internal",
        },
        "email_type": {
            "is_role_email": False,
            "role_type": None,
            "deliverability_risk": "low",
            "confidence": 0.95,
        },
        "security": {
            "in_breach": False,
            "breach_count": 0,
            "risk_level": "low",
            "checked_at": "2025-01-03T12:00:00Z",
            "cached": False,
            "recent_breaches": [],
        },
        "suggested_fixes": {
            "typo_detected": False,
            "suggested_email": None,
            "confidence": 0.0,
            "reason": None,
        },
        "metadata": {
            "timestamp": "2025-01-03T12:00:00Z",
            "validation_id": "val_abc123",
            "request_id": "req_xyz789",
            "cache_used": False,
            "client_plan": "PREMIUM",
        },
    }


@pytest.fixture
def mock_batch_response():
    """Mock batch validation API response"""
    return {
        "count": 3,
        "valid_count": 2,
        "invalid_count": 1,
        "processing_time": 0.45,
        "average_time": 0.15,
        "results": [
            {
                "email": "valid1@example.com",
                "valid": True,
                "detail": "Valid",
                "processing_time": 0.15,
                "risk_score": 0.1,
                "quality_score": 0.9,
                "validation_tier": "standard",
                "suggested_action": "accept",
                "status": "deliverable",
                "provider_analysis": {"provider": "Gmail", "reputation": 0.9},
                "smtp": {"checked": False},
            },
            {
                "email": "valid2@example.com",
                "valid": True,
                "detail": "Valid",
                "processing_time": 0.15,
                "risk_score": 0.15,
                "quality_score": 0.85,
                "validation_tier": "standard",
                "suggested_action": "accept",
                "status": "deliverable",
                "provider_analysis": {"provider": "Yahoo", "reputation": 0.85},
                "smtp": {"checked": False},
            },
            {
                "email": "invalid@test.invalid",
                "valid": False,
                "detail": "Domain does not exist",
                "processing_time": 0.05,
                "risk_score": 0.95,
                "quality_score": 0.05,
                "validation_tier": "basic",
                "suggested_action": "reject",
                "status": "undeliverable",
                "provider_analysis": {"provider": "unknown", "reputation": 0.0},
                "smtp": {"checked": False},
            },
        ],
        "summary": {
            "valid_percentage": 66.67,
            "average_risk_score": 0.4,
        }
    }


@pytest.fixture
def mock_jwt_login_response():
    """Mock JWT login API response"""
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_payload.signature",
        "refresh_token": "refresh_token_abc123",
        "token_type": "bearer",
        "expires_in": 900,  # 15 minutes
    }


@pytest.fixture
def mock_jwt_refresh_response():
    """Mock JWT refresh API response"""
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_payload.signature",
        "refresh_token": "new_refresh_token_xyz789",
        "token_type": "bearer",
        "expires_in": 900,
    }


@pytest.fixture
def mock_usage_response():
    """Mock usage stats API response"""
    return {
        "usage_today": 150,
        "limit": 1000,
        "remaining": 850,
        "usage_percentage": 15.0,
        "plan": "PREMIUM",
        "reset_time": "2025-01-04T00:00:00Z",
        "as_of": "2025-01-03T12:00:00Z",
    }


@pytest.fixture
def sample_emails():
    """Sample email list for testing"""
    return [
        "valid@gmail.com",
        "user@company.com",
        "test@example.org",
        "invalid@",
        "noreply@service.io",
    ]


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file with emails"""
    csv_content = """email,name
test1@example.com,Test User 1
test2@example.com,Test User 2
test3@example.com,Test User 3
"""
    csv_file = tmp_path / "emails.csv"
    csv_file.write_text(csv_content)
    return csv_file


@pytest.fixture
def temp_txt_file(tmp_path):
    """Create a temporary TXT file with emails"""
    txt_content = """test1@example.com
test2@example.com
test3@example.com
"""
    txt_file = tmp_path / "emails.txt"
    txt_file.write_text(txt_content)
    return txt_file
