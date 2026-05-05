"""
LLM provider abstraction layer.

Provides a unified interface for interacting with different LLM APIs
(OpenAI-compatible, Ollama, etc.) with streaming support.
"""

import json
import httpx
from typing import AsyncGenerator, Optional, List, Dict, Any

from .config import ProviderConfig


class Message:
    """Represents a single chat message."""

    def __init__(self, role: str, content: str):
        self.role = role  # "system", "user", "assistant"
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    def __repr__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Message(role={self.role!r}, content={preview!r})"


class LLMProvider:
    """Unified LLM provider with OpenAI-compatible API support."""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self._client: Optional[httpx.AsyncClient] = None

    def _get_headers(self) -> Dict[str, str]:
        """Build request headers."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.config.api_key and self.config.api_key != "ollama":
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _get_chat_url(self) -> str:
        """Build chat completions endpoint URL."""
        base = self.config.base_url.rstrip("/")
        if base.endswith("/v1"):
            return f"{base}/chat/completions"
        return f"{base}/v1/chat/completions"

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Lazily create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout, connect=30.0),
                follow_redirects=True,
            )
        return self._client

    async def chat(
        self,
        messages: List[Message],
        stream: bool = True,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """Send chat messages and yield response chunks.

        Args:
            messages: List of chat messages (system, user, assistant).
            stream: Whether to stream the response.
            temperature: Override provider temperature.
            max_tokens: Override provider max_tokens.

        Yields:
            Response text chunks as strings.
        """
        client = await self._ensure_client()
        url = self._get_chat_url()
        headers = self._get_headers()

        # Build message list with system prompt
        msg_list = []
        if self.config.system_prompt:
            msg_list.append({"role": "system", "content": self.config.system_prompt})
        for msg in messages:
            msg_list.append(msg.to_dict())

        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": msg_list,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": stream,
        }

        if stream:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        delta = data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
        else:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            yield content

    async def test_connection(self) -> tuple[bool, str]:
        """Test connection to the LLM provider.

        Returns:
            Tuple of (success, message).
        """
        try:
            client = await self._ensure_client()
            url = self._get_chat_url()
            headers = self._get_headers()
            payload = {
                "model": self.config.model,
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5,
                "stream": False,
            }
            response = await client.post(url, json=payload, headers=headers, timeout=15.0)
            if response.status_code == 200:
                return True, f"Connected to {self.config.model} successfully"
            else:
                return False, f"HTTP {response.status_code}: {response.text[:200]}"
        except httpx.ConnectError:
            return False, f"Cannot connect to {self.config.base_url}"
        except httpx.TimeoutException:
            return False, f"Connection timed out to {self.config.base_url}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
