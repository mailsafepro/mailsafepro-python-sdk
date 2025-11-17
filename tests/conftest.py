"""
Pytest configuration and shared fixtures
"""
import pytest
from unittest.mock import Mock
from datetime import datetime


@pytest.fixture
def mock_validation_response():
    """Mock successful validation API response"""
    return {
        "email": "test@example.com",
        "valid": True,
        "format_valid": True,
        "disposable": False,
        "role_email": False,
        "free_email": False,
        "status": "valid",
        "risk_score": 10,
        "quality_score": 95,
        "suggested_action": "accept",
        "smtp": {"deliverable": True, "full_inbox": False, "catch_all": False, "disabled": False},
        "dns": {"valid": True, "has_mx": True, "has_spf": True, "has_dmarc": True},
        "provider": {"name": "Example Provider", "domain": "example.com", "type": "business", "reputation_score": 90},
        "security": {"spam_trap": False, "has_known_breaches": False, "breach_count": 0},
        "metadata": {"processing_time_ms": 150, "timestamp": "2025-11-17T20:00:00Z"},
    }


@pytest.fixture
def mock_batch_response():
    """Mock batch validation API response"""
    return {
        "count": 3,
        "valid_count": 2,  # ✅ Agregar este campo
        "invalid_count": 1,  # ✅ Agregar este campo
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
                "status": "valid",
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
                "status": "valid",
                "provider_analysis": {"provider": "Yahoo", "reputation": 0.85},
                "smtp": {"checked": False},
            },
            {
                "email": "invalid@test.com",
                "valid": False,
                "detail": "Invalid",
                "processing_time": 0.05,
                "risk_score": 0.85,
                "quality_score": 0.15,
                "validation_tier": "basic",
                "suggested_action": "reject",
                "status": "invalid",
                "provider_analysis": {"provider": "unknown", "reputation": 0.5},
                "smtp": {"checked": False},
            },
        ],
    }


@pytest.fixture
def mock_jwt_login_response():
    """Mock JWT login API response"""
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
        "refresh_token": "refresh_token_123",
        "token_type": "bearer",
        "expires_in": 3600,
    }


@pytest.fixture
def mock_jwt_refresh_response():
    """Mock JWT refresh API response"""
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_token",
        "token_type": "bearer",
        "expires_in": 3600,
    }
