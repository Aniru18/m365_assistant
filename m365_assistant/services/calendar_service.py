from datetime import datetime, timedelta, timezone
from typing import Any
from ..core.graph_client import GraphClient


class CalendarService:
    def __init__(self, client: GraphClient):
        self.client = client

    def list_upcoming_events(
        self,
        days_ahead: int = 7,
        limit: int = 20,
    ) -> Any:
        """
        List upcoming calendar events.
        Returns authentication instructions if auth is required.
        """

        # 🔥 Step 1 — Authentication check
        headers = self.client._headers()

        if isinstance(headers, dict) and headers.get("status") != "success":
            return headers

        # 🔥 Step 2 — Date range
        now = datetime.now(timezone.utc)
        end_date = now + timedelta(days=days_ahead)

        response = self.client._client.get(
            f"{self.client.settings.graph_base_url}/me/calendarView",
            headers={
                "Authorization": headers["Authorization"]
            },
            params={
                "startDateTime": now.isoformat(),
                "endDateTime": end_date.isoformat(),
                "$top": limit,
                "$orderby": "start/dateTime",
            },
        )

        response.raise_for_status()

        return response.json().get("value", [])

