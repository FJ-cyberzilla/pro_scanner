import httpx
from typing import Dict, Any

from .__init__ import BaseDetector
from src.net.user_agents import UserAgentManager

class RedditDetector(BaseDetector):
    SITE_NAME = "Reddit"
    BASE_URL = "https://www.reddit.com/user"

    async def scan(self, username: str) -> Dict[str, Any]:
        """
        Scans Reddit for the given username.
        """
        profile_url = f"{self.BASE_URL}/{username}"

        try:
            headers = UserAgentManager.get_random_profile()
            async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
                response = await client.get(profile_url)
                
                if response.status_code == 200:
                    # A non-existent user will redirect to the home page or a 404 page
                    if "user not found" in response.text.lower():
                        return self.format_result(status="NOT_FOUND")
                    # Successful profile page usually contains the username
                    elif f"u/{username}" in response.text:
                        return self.format_result(status="FOUND")

                # The `no-profile-page` or 404 response
                if response.status_code == 404:
                    return self.format_result(status="NOT_FOUND")

        except httpx.HTTPError as e:
            return self.format_result(status="ERROR", error=f"HTTP Error: {e}")

        return self.format_result(status="NOT_FOUND")
