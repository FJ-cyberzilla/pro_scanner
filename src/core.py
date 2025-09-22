import asyncio
import httpx
import yaml
from typing import Dict, List, Any

from src.net.http_client import AsyncHttpClient
from src.net.user_agents import UserAgentManager
from src.detectors.instagram import InstagramDetector
from src.db.database_manager import DatabaseManager
from src.utils.cli_utils import ProgressBar

class ProScannerCore:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.http_client = AsyncHttpClient()
        
        with open("config/platforms.yaml", "r") as f:
            self.platforms = yaml.safe_load(f)["platforms"]

    async def scan_username(self, username: str) -> Dict[str, Any]:
        """Orchestrates the full scan workflow."""
        start_time = asyncio.get_event_loop().time()
        
        # We can add a simple progress bar here
        progress_bar = ProgressBar(total=len(self.platforms), desc="Scanning platforms")
        
        tasks = []
        for site_name, config in self.platforms.items():
            # Create tasks for each platform
            if site_name == "instagram":
                task = self.scan_instagram(username, config, progress_bar)
                tasks.append(task)
            # Add logic for other platforms here (e.g., twitter, github)
        
        results = await asyncio.gather(*tasks)
        
        duration = asyncio.get_event_loop().time() - start_time
        
        # Save session to database
        await self.db_manager.save_session(username, len(results), duration)

        return {
            "username": username,
            "results": results,
            "duration": round(duration, 2)
        }

    async def scan_instagram(self, username: str, config: Dict, progress_bar: ProgressBar) -> Dict:
        """Handles the specific Instagram scanning logic."""
        full_url = config["api_url"].format(username)
        headers = UserAgentManager.get_random_profile()
        
        response = await self.http_client.get(full_url, headers=headers)
        
        if response.status_code == 200:
            raw_data = response.json()
            if raw_data.get("user"):
                detector = InstagramDetector()
                details = await detector.get_details({"data": {"user": raw_data["user"]}})
                
                if details:
                    # Logic to download profile picture
                    # ...
                    status = "FOUND"
                    self.db_manager.save_result(username, "instagram", status, details)
                else:
                    status = "NOT_FOUND"
            else:
                status = "NOT_FOUND"
        else:
            status = "ERROR"
        
        progress_bar.update()
        
        return {
            "site": "Instagram",
            "status": status,
            "url": full_url
        }

