from fastmcp import FastMCP
from ..core.config import Settings
from ..core.auth_manager import AuthManager
from ..core.graph_client import GraphClient
from ..services.mail_service import MailService
from ..services.calendar_service import CalendarService


mcp = FastMCP("m365-assistant")
settings = Settings.load()
auth = AuthManager(settings)
client = GraphClient(auth, settings)
mail_service = MailService(client)
calendar_service = CalendarService(client)


@mcp.tool
def list_emails(limit: int = 20):
    """List emails from last 5 days."""
    return mail_service.list_last_n_days(days=5, limit=limit)
@mcp.tool
def list_upcoming_events(days_ahead: int = 7, limit: int = 20):
    """List upcoming calendar events."""
    return calendar_service.list_upcoming_events(
        days_ahead=days_ahead,
        limit=limit
    )
@mcp.tool
def forward_email(email_id: str, to: list[str], comment: str | None = None):
    """
    Forward an existing email to one or more recipients.

    Use this tool when the user asks to forward a specific email
    to other people.
    """
    return mail_service.forward_email(email_id, to, comment)


@mcp.tool
def reply_all_email(email_id: str, body: str):
    """
    Reply to all recipients of a specific email.

    Use this tool when the user says 'reply all'.
    """
    return mail_service.reply_all_email(email_id, body)


@mcp.tool
def flag_email(email_id: str, status: str = "flagged"):
    """
    Flag or unflag an email.

    status options:
    - flagged
    - complete
    - notFlagged
    """
    return mail_service.flag_email(email_id, status)
@mcp.tool
def mark_email_as_read(email_id: str):
    """
    Mark an email as read.

    Use when the user says:
    - "Mark this email as read"
    - "Mark the last email as read"
    """
    return mail_service.mark_email_read(email_id)
@mcp.tool
def mark_email_as_unread(email_id: str):
    """
    Mark an email as unread.

    Use when the user wants to keep it for later.
    """
    return mail_service.mark_email_unread(email_id)
@mcp.tool
def reply_to_specific_recipient(
    original_email_id: str,
    recipient: str,
    body: str,
    subject: str | None = None,
):
    """
    Reply to a specific recipient only.

    This is useful when the user wants to respond to
    only one person instead of using reply-all.
    """
    return mail_service.reply_to_recipient(
        original_email_id,
        recipient,
        body,
        subject,
    )


@mcp.tool
def create_mail_folder(folder_name: str):
    """
    Create a new folder in the mailbox.

    Use when user asks to organize emails into folders.
    """
    return mail_service.create_mail_folder(folder_name)

@mcp.tool
def list_calendar_events(days_ahead: int = 7, limit: int = 20):
    """
    List upcoming calendar events within a date range.

    Use when user asks about meetings or schedule.
    """
    return calendar_service.list_events(days_ahead, limit)
