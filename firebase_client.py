# firebase_client.py
import os
import json
import threading
import firebase_admin
from firebase_admin import credentials, db

# Single initialization guard (thread-safe)
_lock = threading.Lock()
_app = None
print("🔥 Firebase initialized successfully with project:", os.getenv("FIREBASE_PROJECT_ID"))

def _load_service_account() -> dict:
    svc = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if not svc:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT is missing from environment.")

    try:
        sa: dict = json.loads(svc)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT is not valid JSON. "
            "Did you wrap it in quotes properly in .env?"
        ) from e

    # Fix common issue where private_key has literal '\n' instead of newlines
    if "private_key" in sa and "\\n" in sa["private_key"]:
        sa["private_key"] = sa["private_key"].replace("\\n", "\n")

    required_keys = ("type", "project_id", "private_key", "client_email")
    missing = [k for k in required_keys if not sa.get(k)]
    if missing:
        raise RuntimeError(
            f"FIREBASE_SERVICE_ACCOUNT JSON missing keys: {', '.join(missing)}"
        )

    return sa

def init_firebase():
    """
    Initialize firebase_admin once and reuse.
    Respects:
      - FIREBASE_DATABASE_URL  (required, unless using emulator)
      - FIREBASE_PROJECT_ID    (recommended)
      - FIREBASE_EMULATOR_HOST (optional; enables RTDB emulator)
    """
    global _app
    if _app is not None:
        return _app

    with _lock:
        if _app is not None:
            return _app

        # Emulator support (optional)
        emulator_host = os.getenv("FIREBASE_EMULATOR_HOST", "").strip()
        db_url = os.getenv("FIREBASE_DATABASE_URL", "").strip()

        if emulator_host:
            # When using emulator, databaseURL must be http://<host> (no https)
            # Example: FIREBASE_EMULATOR_HOST=localhost:9000
            db_url = f"http://{emulator_host}/?ns={os.getenv('FIREBASE_PROJECT_ID')}"
            # In emulator mode, creds can be anything; still load to keep code uniform.
            sa = _load_service_account()
            cred = credentials.Certificate(sa)
        else:
            if not db_url:
                raise RuntimeError(
                    "FIREBASE_DATABASE_URL is missing. "
                    "Set it in your .env (or set FIREBASE_EMULATOR_HOST to use emulator)."
                )
            sa = _load_service_account()
            cred = credentials.Certificate(sa)

        opts = {
            "databaseURL": db_url
        }
        # Optional but nice to have
        project_id = os.getenv("FIREBASE_PROJECT_ID")
        if project_id:
            opts["projectId"] = project_id

        # Create / reuse default app
        if not firebase_admin._apps:  # type: ignore[attr-defined]
            _app = firebase_admin.initialize_app(cred, opts)
        else:
            _app = firebase_admin.get_app()

        return _app

def rtdb():
    """Return the firebase_admin db module (after ensuring init)."""
    init_firebase()
    return db

def ref(path: str):
    """Shorthand to get a DatabaseReference for a path."""
    return rtdb().reference(path)
