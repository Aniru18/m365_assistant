import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    client_id: str
    authority: str
    graph_base_url: str = "https://graph.microsoft.com/v1.0"

    @staticmethod
    def load() -> "Settings":
        client_id = os.getenv("MICROSOFT_CLIENT_ID")

        if not client_id:
            raise RuntimeError("MICROSOFT_CLIENT_ID not configured")

        return Settings(
            client_id=client_id,
            authority="https://login.microsoftonline.com/common",
        )
