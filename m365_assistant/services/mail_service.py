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

        #  Step 1 — Check authentication first
        headers = self.client._headers()

        # If auth not successful, return auth instructions immediately
        if isinstance(headers, dict) and headers.get("status") != "success":
            return headers

        #  Step 2 — Compute date filter
        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=days)
        ).isoformat()

        #  Step 3 — Call Graph API
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
    
    def mark_email_read(self, email_id: str) -> Any:
        """
        Mark a specific email as read.
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
            json={"isRead": True},
        )

        response.raise_for_status()
        return {"status": "marked_as_read"}
    def mark_email_unread(self, email_id: str) -> Any:
        """
        Mark a specific email as unread.
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
            json={"isRead": False},
        )

        response.raise_for_status()
        return {"status": "marked_as_unread"}
    def reply_to_recipient(
        self,
        original_email_id: str,
        recipient: str,
        body: str,
        subject: str | None = None,
    ) -> Any:
        """
        Reply to a specific recipient only.

        This does NOT use reply or replyAll endpoint.
        Instead, it sends a new message referencing the original email.
        """

        headers = self.client._headers()
        if headers.get("status") != "success":
            return headers

        # Fetch original email for subject reference if needed
        original = self.get_email(original_email_id)

        if isinstance(original, dict) and original.get("status") != "success":
            return original

        final_subject = subject or f"Re: {original.get('subject', '')}"

        payload = {
            "message": {
                "subject": final_subject,
                "body": {
                    "contentType": "Text",
                    "content": body,
                },
                "toRecipients": [
                    {"emailAddress": {"address": recipient}}
                ],
            }
        }

        response = self.client._client.post(
            f"{self.client.settings.graph_base_url}/me/sendMail",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": "application/json",
            },
            json=payload,
        )

        response.raise_for_status()
        return {"status": "sent_to_specific_recipient"}
