import json
from typing import Dict, Any, Optional

class InstagramDetector:
    async def get_details(self, response: Dict[str, Any]) -> Optional[Dict]:
        """Parses the Instagram API response using a robust method."""
        try:
            user_data = response.get("data", {}).get("user", {})
            if not user_data:
                return None

            details = {
                "username": user_data.get("username"),
                "full_name": user_data.get("full_name"),
                "user_id": user_data.get("id"),
                "followers": user_data.get("edge_followed_by", {}).get("count"),
                "following": user_data.get("edge_follow", {}).get("count"),
                "posts": user_data.get("edge_owner_to_timeline_media", {}).get("count"),
                "is_private": user_data.get("is_private"),
                "is_verified": user_data.get("is_verified"),
                "profile_pic_url": user_data.get("profile_pic_url"),
            }
            return details
        except (KeyError, AttributeError, json.JSONDecodeError) as e:
            # Log the error for debugging
            print(f"Error parsing Instagram data: {e}")
            return None
          
