import httpx
from typing import Dict, Any, Optional

from .__init__ import BaseDetector
from src.net.user_agents import UserAgentManager

class BskyAppDetector(BaseDetector):
    SITE_NAME = "Bluesky Social"
    BASE_URL = "https://public.api.bsky.app"

    async def scan(self, username: str) -> Dict[str, Any]:
        """
        Scans Bluesky for the given username.
        Uses the com.atproto.identity.resolveHandle API endpoint.
        """
        api_endpoint = f"{self.BASE_URL}/xrpc/com.atproto.identity.resolveHandle?handle={username}.bsky.social"
        
        try:
            headers = UserAgentManager.get_random_profile()
            async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
                response = await client.get(api_endpoint)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'did' in data:
                        # User handle exists and was resolved to a DID
                        return self.format_result(
                            status="FOUND",
                            details={"did": data['did']}
                        )
                
                # If status code is 400 (Bad Request), handle is not found
                elif response.status_code == 400:
                    return self.format_result(status="NOT_FOUND")

                # Handle other HTTP errors
                response.raise_for_status()
                
        except httpx.HTTPError as e:
            return self.format_result(status="ERROR", error=f"HTTP Error: {e}")
        except Exception as e:
            return self.format_result(status="ERROR", error=f"Unexpected Error: {e}")

        return self.format_result(status="NOT_FOUND")
