"""
MailSafePro Client - Main API client with authentication support (Sync & Async)
"""

import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Type, TypeVar, Generator, AsyncGenerator
from dataclasses import dataclass

import httpx
from pydantic import ValidationError as PydanticValidationError

from .exceptions import (
    EmailValidatorError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    QuotaExceededError,
    ServerError,
    NetworkError,
)
from .models import (
    ValidationResult,
    BatchResult,
    UsageStats,
)
from .utils import validate_email_format, validate_file_path

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class ClientConfig:
    """Configuration for MailSafePro Client"""
    api_key: Optional[str] = None
    base_url: str = "https://api.mailsafepro.com"
    timeout: int = 30
    max_retries: int = 3
    enable_logging: bool = False


class BaseClient:
    """Base client with shared logic for Sync and Async clients"""

    USER_AGENT = "MailSafePro-Python-SDK/2.1.0"

    def __init__(self, config: Optional[ClientConfig] = None, **kwargs):
        if config is None:
            config = ClientConfig(**kwargs)
        
        self.config = config
        self.base_url = config.base_url.rstrip("/")
        self._api_key = config.api_key

        # JWT token management
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

        if config.enable_logging:
            logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        logger.debug(f"MailSafePro initialized: base_url={self.base_url}")

    @property
    def timeout(self) -> int:
        return self.config.timeout

    @property
    def max_retries(self) -> int:
        return self.config.max_retries

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers (API Key or JWT)"""
        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        elif self._api_key:
            headers["X-API-Key"] = self._api_key

        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise exceptions if needed"""
        request_id = response.headers.get("X-Request-ID")
        
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            
            data = response.json()
            # Inject request_id into metadata if present in response structure
            if isinstance(data, dict) and "metadata" in data:
                if isinstance(data["metadata"], dict):
                    data["metadata"]["request_id"] = request_id
            
            return data

        except httpx.HTTPStatusError as e:
            status_code = response.status_code
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except Exception:
                pass

            if status_code == 401:
                raise AuthenticationError(error_detail, request_id)
            elif status_code == 403:
                if "quota" in str(error_detail).lower() or "limit" in str(error_detail).lower():
                    raise QuotaExceededError(error_detail, request_id)
                raise AuthenticationError(error_detail, request_id)
            elif status_code == 422:
                raise ValidationError(error_detail, request_id)
            elif status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(
                    f"Rate limit exceeded. Retry after {retry_after} seconds",
                    retry_after=retry_after,
                )
            elif status_code >= 500:
                raise ServerError(f"Server error: {status_code}", status_code=status_code)
            
            raise EmailValidatorError(f"Request failed: {error_detail}", request_id) from e
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}", request_id) from e
        except Exception as e:
            raise EmailValidatorError(f"Unexpected error: {str(e)}", request_id) from e

    def _chunk_list(self, items: List[T], chunk_size: int) -> Generator[List[T], None, None]:
        """Yield successive chunks from items."""
        for i in range(0, len(items), chunk_size):
            yield items[i : i + chunk_size]


class MailSafePro(BaseClient):
    """
    Synchronous MailSafePro Client
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # Support both config object and direct kwargs
        if "config" in kwargs:
            super().__init__(kwargs["config"])
        else:
            # Filter out None values to let ClientConfig defaults take over
            clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
            super().__init__(ClientConfig(api_key=api_key, **clean_kwargs))
            
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.config.timeout,
            transport=httpx.HTTPTransport(retries=self.config.max_retries),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._client.close()

    @classmethod
    def login(
        cls,
        username: str,
        password: str,
        base_url: Optional[str] = None,
        **kwargs
    ) -> "MailSafePro":
        instance = cls(base_url=base_url, **kwargs)
        try:
            response = instance._client.post(
                "/auth/login",
                json={"email": username, "password": password},
            )
            data = instance._handle_response(response)
            
            instance._access_token = data.get("access_token")
            instance._refresh_token = data.get("refresh_token")
            expires_in = data.get("expires_in", 900)
            instance._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return instance
        except Exception as e:
            instance.close()
            request_id = getattr(e, "request_id", None)
            raise AuthenticationError(f"Login failed: {str(e)}", request_id) from e

    def _refresh_token_if_needed(self):
        if self._access_token and self._token_expires_at and datetime.now() >= self._token_expires_at:
            if not self._refresh_token:
                raise AuthenticationError("No refresh token available")
            try:
                response = self._client.post(
                    "/auth/refresh",
                    headers={"Authorization": f"Bearer {self._refresh_token}"}
                )
                data = self._handle_response(response)
                self._access_token = data.get("access_token")
                self._refresh_token = data.get("refresh_token")
                expires_in = data.get("expires_in", 900)
                self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            except Exception as e:
                raise AuthenticationError(f"Token refresh failed: {str(e)}") from e

    def validate(
        self,
        email: str,
        check_smtp: bool = False,
        include_raw_dns: bool = False,
        priority: str = "standard",
    ) -> ValidationResult:
        self._refresh_token_if_needed()
        validate_email_format(email)
        
        payload = {
            "email": email,
            "check_smtp": check_smtp,
            "include_raw_dns": include_raw_dns,
            "priority": priority,
        }
        
        response = self._client.post(
            "/validate/email",
            json=payload,
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return ValidationResult.model_validate(data)

    def validate_batch(
        self,
        emails: List[str],
        check_smtp: bool = False,
        include_raw_dns: bool = False,
        batch_size: int = 100,
        concurrent_requests: int = 5,
    ) -> BatchResult:
        self._refresh_token_if_needed()
        if not emails:
            raise ValidationError("Email list cannot be empty")

        MAX_BATCH_SIZE = 10000
        
        # Auto-chunking logic
        if len(emails) > MAX_BATCH_SIZE:
            logger.info(f"Input list size ({len(emails)}) exceeds limit ({MAX_BATCH_SIZE}). Auto-chunking...")
            all_results = []
            total_processed = 0
            total_valid = 0
            total_invalid = 0
            start_time = time.time()
            
            for chunk in self._chunk_list(emails, MAX_BATCH_SIZE):
                chunk_result = self.validate_batch(
                    chunk, check_smtp, include_raw_dns, batch_size, concurrent_requests
                )
                all_results.extend(chunk_result.results)
                total_processed += chunk_result.count
                total_valid += chunk_result.valid_count
                total_invalid += chunk_result.invalid_count
                
            total_time = time.time() - start_time
            
            return BatchResult(
                count=total_processed,
                valid_count=total_valid,
                invalid_count=total_invalid,
                processing_time=total_time,
                average_time=total_time / total_processed if total_processed > 0 else 0,
                results=all_results,
                summary={"chunked": True, "chunks": (len(emails) // MAX_BATCH_SIZE) + 1}
            )

        payload = {
            "emails": emails,
            "check_smtp": check_smtp,
            "include_raw_dns": include_raw_dns,
            "batch_size": batch_size,
            "concurrent_requests": concurrent_requests,
        }

        response = self._client.post(
            "/batch",
            json=payload,
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return BatchResult.model_validate(data)

    def validate_file(
        self,
        file_path: Union[str, Path],
        column: Optional[str] = None,
        check_smtp: bool = False,
        include_raw_dns: bool = False,
    ) -> BatchResult:
        self._refresh_token_if_needed()
        file_path = validate_file_path(file_path)
        
        data_params = {
            "check_smtp": str(check_smtp).lower(),
            "include_raw_dns": str(include_raw_dns).lower(),
        }
        if column:
            data_params["column"] = column

        headers = self._get_auth_headers()
        headers.pop("Content-Type", None)

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f)}
            response = self._client.post(
                "/batch/upload",
                data=data_params,
                files=files,
                headers=headers
            )
            data = self._handle_response(response)
            return BatchResult.model_validate(data)

    def get_usage(self) -> UsageStats:
        self._refresh_token_if_needed()
        response = self._client.get(
            "/usage",
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return UsageStats.model_validate(data)

    def get_quota(self) -> Dict[str, Any]:
        """Deprecated: Use get_usage() instead"""
        logger.warning("get_quota() is deprecated, use get_usage() instead")
        return self.get_usage().model_dump()


class AsyncMailSafePro(BaseClient):
    """
    Asynchronous MailSafePro Client
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        if "config" in kwargs:
            super().__init__(kwargs["config"])
        else:
            clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
            super().__init__(ClientConfig(api_key=api_key, **clean_kwargs))
            
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.config.timeout,
            transport=httpx.AsyncHTTPTransport(retries=self.config.max_retries),
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._client.aclose()

    @classmethod
    async def login(
        cls,
        username: str,
        password: str,
        base_url: Optional[str] = None,
        **kwargs
    ) -> "AsyncMailSafePro":
        instance = cls(base_url=base_url, **kwargs)
        try:
            response = await instance._client.post(
                "/auth/login",
                json={"email": username, "password": password},
            )
            data = instance._handle_response(response)
            
            instance._access_token = data.get("access_token")
            instance._refresh_token = data.get("refresh_token")
            expires_in = data.get("expires_in", 900)
            instance._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return instance
        except Exception as e:
            await instance.close()
            request_id = getattr(e, "request_id", None)
            raise AuthenticationError(f"Login failed: {str(e)}", request_id) from e

    async def _refresh_token_if_needed(self):
        if self._access_token and self._token_expires_at and datetime.now() >= self._token_expires_at:
            if not self._refresh_token:
                raise AuthenticationError("No refresh token available")
            try:
                response = await self._client.post(
                    "/auth/refresh",
                    headers={"Authorization": f"Bearer {self._refresh_token}"}
                )
                data = self._handle_response(response)
                self._access_token = data.get("access_token")
                self._refresh_token = data.get("refresh_token")
                expires_in = data.get("expires_in", 900)
                self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            except Exception as e:
                raise AuthenticationError(f"Token refresh failed: {str(e)}") from e

    async def validate(
        self,
        email: str,
        check_smtp: bool = False,
        include_raw_dns: bool = False,
        priority: str = "standard",
    ) -> ValidationResult:
        await self._refresh_token_if_needed()
        validate_email_format(email)
        
        payload = {
            "email": email,
            "check_smtp": check_smtp,
            "include_raw_dns": include_raw_dns,
            "priority": priority,
        }
        
        response = await self._client.post(
            "/validate/email",
            json=payload,
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return ValidationResult.model_validate(data)

    async def validate_batch(
        self,
        emails: List[str],
        check_smtp: bool = False,
        include_raw_dns: bool = False,
        batch_size: int = 100,
        concurrent_requests: int = 5,
    ) -> BatchResult:
        await self._refresh_token_if_needed()
        if not emails:
            raise ValidationError("Email list cannot be empty")

        MAX_BATCH_SIZE = 10000
        
        # Auto-chunking logic
        if len(emails) > MAX_BATCH_SIZE:
            logger.info(f"Input list size ({len(emails)}) exceeds limit ({MAX_BATCH_SIZE}). Auto-chunking...")
            all_results = []
            total_processed = 0
            total_valid = 0
            total_invalid = 0
            start_time = time.time()
            
            for chunk in self._chunk_list(emails, MAX_BATCH_SIZE):
                chunk_result = await self.validate_batch(
                    chunk, check_smtp, include_raw_dns, batch_size, concurrent_requests
                )
                all_results.extend(chunk_result.results)
                total_processed += chunk_result.count
                total_valid += chunk_result.valid_count
                total_invalid += chunk_result.invalid_count
                
            total_time = time.time() - start_time
            
            return BatchResult(
                count=total_processed,
                valid_count=total_valid,
                invalid_count=total_invalid,
                processing_time=total_time,
                average_time=total_time / total_processed if total_processed > 0 else 0,
                results=all_results,
                summary={"chunked": True, "chunks": (len(emails) // MAX_BATCH_SIZE) + 1}
            )

        payload = {
            "emails": emails,
            "check_smtp": check_smtp,
            "include_raw_dns": include_raw_dns,
            "batch_size": batch_size,
            "concurrent_requests": concurrent_requests,
        }

        response = await self._client.post(
            "/batch",
            json=payload,
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return BatchResult.model_validate(data)

    async def validate_file(
        self,
        file_path: Union[str, Path],
        column: Optional[str] = None,
        check_smtp: bool = False,
        include_raw_dns: bool = False,
    ) -> BatchResult:
        await self._refresh_token_if_needed()
        file_path = validate_file_path(file_path)
        
        data_params = {
            "check_smtp": str(check_smtp).lower(),
            "include_raw_dns": str(include_raw_dns).lower(),
        }
        if column:
            data_params["column"] = column

        headers = self._get_auth_headers()
        headers.pop("Content-Type", None)

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f)}
            response = await self._client.post(
                "/batch/upload",
                data=data_params,
                files=files,
                headers=headers
            )
            data = self._handle_response(response)
            return BatchResult.model_validate(data)

    async def get_usage(self) -> UsageStats:
        await self._refresh_token_if_needed()
        response = await self._client.get(
            "/usage",
            headers=self._get_auth_headers()
        )
        data = self._handle_response(response)
        return UsageStats.model_validate(data)

    async def get_quota(self) -> Dict[str, Any]:
        """Deprecated: Use get_usage() instead"""
        logger.warning("get_quota() is deprecated, use get_usage() instead")
        usage = await self.get_usage()
        return usage.model_dump()
