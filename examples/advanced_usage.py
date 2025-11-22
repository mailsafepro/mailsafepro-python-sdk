
import asyncio
import json
from unittest.mock import MagicMock, patch
from mailsafepro import MailSafePro, AsyncMailSafePro, UsageStats, ClientConfig, AuthenticationError

def mock_response(data, status_code=200, headers=None):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = data
    mock.headers = headers or {}
    mock.raise_for_status.side_effect = None
    if status_code >= 400:
        # Simulate httpx raising HTTPStatusError
        import httpx
        request = httpx.Request("GET", "http://test")
        mock.raise_for_status.side_effect = httpx.HTTPStatusError(
            f"{status_code} Error", request=request, response=mock
        )
    return mock

def test_advanced_features():
    print("Testing Advanced Features...")
    
    # 1. Test ClientConfig
    config = ClientConfig(api_key="test_key", timeout=10)
    client = MailSafePro(config=config)
    assert client.timeout == 10
    print("✅ ClientConfig initialized correctly")

    # 2. Test Request ID in Exception
    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = mock_response(
            {"detail": "Invalid API Key"}, 
            status_code=401, 
            headers={"X-Request-ID": "req_123"}
        )
        
        try:
            client.login("user", "pass")
        except AuthenticationError as e:
            assert e.request_id == "req_123"
            print(f"✅ Request ID captured in exception: {e.request_id}")

    # 3. Test Auto-Chunking
    with patch("httpx.Client.post") as mock_post:
        # Mock response for batch validation
        mock_post.return_value = mock_response({
            "count": 5000,
            "valid_count": 5000,
            "invalid_count": 0,
            "results": [{"email": "test@example.com", "valid": True}] * 5000
        })
        
        # Create a list larger than 10k
        large_list = ["test@example.com"] * 15000
        
        # We expect 2 calls (10k + 5k)
        result = client.validate_batch(large_list)
        
        assert mock_post.call_count == 2
        assert result.count == 10000 # Mock returns 5000 per call * 2 calls = 10000 (simplified mock logic)
        # Actually, my mock returns 5000 regardless of input size, so 2 calls = 10000 total processed in result
        
        print(f"✅ Auto-chunking triggered (Calls: {mock_post.call_count})")

if __name__ == "__main__":
    try:
        test_advanced_features()
        print("\n🎉 Phase 2 verification passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
