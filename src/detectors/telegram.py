import httpx
from typing import Dict, Any

from .__init__ import BaseDetector
from src.net.user_agents import UserAgentManager

class TelegramDetector(BaseDetector):
    SITE_NAME = "Telegram"
    BASE_URL = "https://t.me"

    async def scan(self, username: str) -> Dict[str, Any]:
        """
        Scans for a Telegram user or channel by checking their public t.me page.
        """
        profile_url = f"{self.BASE_URL}/{username}"

        try:
            headers = UserAgentManager.get_random_profile()
            async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
                response = await client.get(profile_url)
                
                # Telegram pages that don't exist often return a 404 or a page with "Channel not found" text
                if response.status_code == 404 or "channel not found" in response.text.lower() or "user not found" in response.text.lower():
                    return self.format_result(status="NOT_FOUND")
                
                # A successful 200 OK status indicates the profile exists
                elif response.status_code == 200:
                    return self.format_result(status="FOUND")
                
                response.raise_for_status()

        except httpx.HTTPError as e:
            return self.format_result(status="ERROR", error=f"HTTP Error: {e}")
        except Exception as e:
            return self.format_result(status="ERROR", error=f"Unexpected Error: {e}")
            
        return self.format_result(status="NOT_FOUND")

