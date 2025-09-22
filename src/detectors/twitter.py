import httpx
import logging
from typing import Dict, Any

from .__init__ import BaseDetector
from src.net.user_agents import UserAgentManager

logger = logging.getLogger(__name__)

class TwitterDetector(BaseDetector):
    SITE_NAME = "Twitter/X"
    BASE_URL = "https://twitter.com"

    async def scan(self, username: str) -> Dict[str, Any]:
        """
        Scans Twitter for the given username using web scraping.
        Note: This is highly prone to being blocked. An API key is better.
        """
        profile_url = f"{self.BASE_URL}/{username}"

        try:
            headers = UserAgentManager.get_random_profile()
            async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
                response = await client.get(profile_url)
                
                # Twitter redirects to its own 404 page if a user doesn't exist
                if "page isn't available" in response.text:
                    return self.format_result(status="NOT_FOUND")
                
                # A 200 OK status indicates the profile page loaded successfully
                elif response.status_code == 200:
                    return self.format_result(status="FOUND")
                    
                response.raise_for_status()
                
        except httpx.HTTPError as e:
            return self.format_result(status="ERROR", error=f"HTTP Error: {e}")
        except Exception as e:
            return self.format_result(status="ERROR", error=f"Unexpected Error: {e}")
            
        return self.format_result(status="NOT_FOUND")
