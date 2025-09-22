import random
from typing import Dict, List

class UserAgentManager:
    _PROFILES: List[Dict] = [
        # Modern Chrome Desktop on Windows
        {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec_ch_ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec_ch_ua_platform": '"Windows"'
        },
        # Modern Chrome on macOS
        {
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec_ch_ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec_ch_ua_platform": '"macOS"'
        },
        # Firefox on Linux
        {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        },
        # Safari on macOS
        {
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        },
        # Mobile Chrome on Android
        {
            "user_agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "sec_ch_ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec_ch_ua_platform": '"Android"',
            "sec_ch_ua_mobile": "?1"
        },
    ]

    @classmethod
    def get_random_profile(cls) -> Dict[str, str]:
        profile = random.choice(cls._PROFILES)
        headers = {
            "User-Agent": profile["user_agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",
            "Connection": "keep-alive"
        }
        if "sec_ch_ua" in profile:
            headers.update({
                "Sec-Ch-Ua": profile["sec_ch_ua"],
                "Sec-Ch-Ua-Mobile": profile.get("sec_ch_ua_mobile", "?0"),
                "Sec-Ch-Ua-Platform": profile["sec_ch_ua_platform"]
            })
        return headers
      
