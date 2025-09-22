import httpx
import asyncio
import logging
from typing import Dict, Any, Optional

# Set up logging for the HTTP client
logger = logging.getLogger(__name__)

class AsyncHttpClient:
    """
    An asynchronous HTTP client for all network requests.
    Manages a single httpx.AsyncClient instance for efficient connection pooling.
    """
    
    _instance = None
    _client: Optional[httpx.AsyncClient] = None
    
    # Use a lock to prevent race conditions during instance creation in a threaded environment
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls):
        """Returns a singleton instance of the client."""
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    await cls._instance._init_client()
        return cls._instance

    async def _init_client(self):
        """Initializes the httpx.AsyncClient."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
            logger.info("HTTP client initialized successfully.")

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Performs an asynchronous GET request."""
        try:
            return await self._client.get(url, **kwargs)
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {url}: {e}")
            raise
        except httpx.TimeoutException as e:
            logger.error(f"Request to {url} timed out: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting {url}: {e}")
            raise

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """Performs an asynchronous POST request."""
        try:
            return await self._client.post(url, **kwargs)
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {url}: {e}")
            raise
        except httpx.TimeoutException as e:
            logger.error(f"Request to {url} timed out: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"An error occurred while posting to {url}: {e}")
            raise
            
    async def close(self):
        """Closes the client session."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("HTTP client session closed.")

