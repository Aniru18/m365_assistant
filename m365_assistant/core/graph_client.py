import httpx
from typing import Optional, Dict, Any
from .auth_manager import AuthManager
from .config import Settings


class GraphClient:
    def __init__(self, auth: AuthManager, settings: Settings):
        self.auth = auth
        self.settings = settings
        self._client = httpx.Client(timeout=30)

    def _headers(self):
        result = self.auth.acquire_token()

        if result["status"] != "success":
            return result

        return {
            "status": "success",
            "Authorization": f"Bearer {result['access_token']}"
        }


    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        response = self._client.get(
            f"{self.settings.graph_base_url}{path}",
            headers=self._headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()
