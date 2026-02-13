import pathlib
import msal
from typing import Optional
from .config import Settings

CACHE_FILE = pathlib.Path.home() / ".m365_token_cache.json"
SCOPES = ["https://graph.microsoft.com/.default"]


class AuthManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._cache = msal.SerializableTokenCache()
        self._pending_flow = None

        if CACHE_FILE.exists():
            self._cache.deserialize(CACHE_FILE.read_text())

        self._app = msal.PublicClientApplication(
            settings.client_id,
            authority=settings.authority,
            token_cache=self._cache,
        )

    def _save_cache(self):
        if self._cache.has_state_changed:
            CACHE_FILE.write_text(self._cache.serialize())

    def acquire_token(self):

        accounts = self._app.get_accounts()
        account = accounts[0] if accounts else None

        #  Try silent first
        result = self._app.acquire_token_silent(SCOPES, account=account)

        if result and "access_token" in result:
            return {"status": "success", "access_token": result["access_token"]}

        #  If device flow already started → try completing it
        if self._pending_flow:
            result = self._app.acquire_token_by_device_flow(self._pending_flow)

            if "access_token" in result:
                self._pending_flow = None
                self._save_cache()
                return {"status": "success", "access_token": result["access_token"]}

            return {
                "status": "authentication_pending",
                "message": "Authentication still pending. Please complete login."
            }

        #  Start new device flow
        flow = self._app.initiate_device_flow(scopes=SCOPES)

        if "user_code" not in flow:
            raise RuntimeError("Failed to initiate device flow")

        self._pending_flow = flow

        return {
            "status": "authentication_required",
            "verification_uri": flow["verification_uri"],
            "user_code": flow["user_code"],
            "message": "Please authenticate, then call the tool again."
        }
