from datetime import datetime, timedelta, timezone
from typing import Any, Dict,List
from ..core.graph_client import GraphClient


class MailService:
    def __init__(self, client: GraphClient):
        self.client = client

    def list_last_n_days(self, days: int = 5, limit: int = 20) -> Any:
        """
        List inbox emails from the last N days.
        If authentication is required, returns authentication instructions.
        """

        # 🔥 Step 1 — Check authentication first
        headers = self.client._headers()

        # If auth not successful, return auth instructions immediately
        if isinstance(headers, dict) and headers.get("status") != "success":
            return headers

        # 🔥 Step 2 — Compute date filter
        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=days)
        ).isoformat()

        # 🔥 Step 3 — Call Graph API
        response = self.client._client.get(
            f"{self.client.settings.graph_base_url}/me/mailFolders/inbox/messages",
            headers={
                "Authorization": f"Bearer {headers['Authorization'].split(' ')[1]}"
            },
            params={
                "$top": limit,
                "$filter": f"receivedDateTime ge {cutoff}",
                "$orderby": "receivedDateTime desc",
            },
        )

        response.raise_for_status()

        return response.json().get("value", [])



    def forward_email(self, email_id: str, to: List[str], 
                      comment: str | None = None) -> Any:
        """
        Forward an existing email to new recipients.

        Args:
            email_id: The Microsoft Graph ID of the email to forward.
            to: List of recipient email addresses.
            comment: Optional message to include when forwarding.
        """

        headers = self.client._headers()
        if headers.get("status") != "success":
            return headers

        payload = {
            "toRecipients": [
                {"emailAddress": {"address": addr}} for addr in to
            ]
        }

        if comment:
            payload["comment"] = comment

        response = self.client._client.post(
            f"{self.client.settings.graph_base_url}/me/messages/{email_id}/forward",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": "application/json",
            },
            json=payload,
        )

        response.raise_for_status()
        return {"status": "forwarded"}


    def reply_all_email(self, email_id: str, body: str) -> Any:
        """
        Reply to all recipients of a specific email.
        """

        headers = self.client._headers()
        if headers.get("status") != "success":
            return headers

        payload = {
            "message": {
                "body": {
                    "contentType": "Text",
                    "content": body,
                }
            }
        }

        response = self.client._client.post(
            f"{self.client.settings.graph_base_url}/me/messages/{email_id}/replyAll",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": "application/json",
            },
            json=payload,
        )

        response.raise_for_status()
        return {"status": "replied_all"}


    def flag_email(self, email_id: str, status: str = "flagged") -> Any:
        """
        Flag an email for follow-up.

        Status can be:
            - 'flagged'
            - 'complete'
            - 'notFlagged'
        """

        headers = self.client._headers()
        if headers.get("status") != "success":
            return headers

        response = self.client._client.patch(
            f"{self.client.settings.graph_base_url}/me/messages/{email_id}",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": "application/json",
            },
            json={
                "flag": {
                    "flagStatus": status
                }
            },
        )

        response.raise_for_status()
        return {"status": status}


    def create_mail_folder(self, folder_name: str) -> Any:
        """
        Create a new mail folder in the user's mailbox.
        """

        headers = self.client._headers()
        if headers.get("status") != "success":
            return headers

        response = self.client._client.post(
            f"{self.client.settings.graph_base_url}/me/mailFolders",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": "application/json",
            },
            json={"displayName": folder_name},
        )

        response.raise_for_status()
        return response.json()
