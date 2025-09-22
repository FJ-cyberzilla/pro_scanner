import httpx
from typing import Dict, Any

from .__init__ import BaseDetector
from src.net.user_agents import UserAgentManager

class PinterestDetector(BaseDetector):
    SITE_NAME = "Pinterest"
    BASE_URL = "https://www.pinterest.com"

    async def scan(self, username: str) -> Dict[str, Any]:
        """
        Scans Pinterest for the given username by checking their public profile page.
        """
        profile_url = f"{self.BASE_URL}/{username}"

        try:
            headers = UserAgentManager.get_random_profile()
            async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
                response = await client.get(profile_url)

                # A 200 OK status indicates the profile page exists
                if response.status_code == 200:
                    # Pinterest sometimes returns a generic page for nonexistent users.
                    # We can check for a specific keyword in the HTML.
                    if "Sorry, we couldn't find a page at this URL" in response.text:
                         return self.format_result(status="NOT_FOUND")
                    else:
                        return self.format_result(status="FOUND")
                
                # A 404 status code directly indicates the profile does not exist
                elif response.status_code == 404:
                    return self.format_result(status="NOT_FOUND")
                
                response.raise_for_status()

        except httpx.HTTPError as e:
            return self.format_result(status="ERROR", error=f"HTTP Error: {e}")
        except Exception as e:
            return self.format_result(status="ERROR", error=f"Unexpected Error: {e}")
            
        return self.format_result(status="NOT_FOUND")
