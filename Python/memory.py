# memory.py 

import time
from config import SESSION_TTL_SECONDS

_sessions = {}

def get_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        return None, True

    is_expired = (time.time() - session["lastFetchedAt"]) > SESSION_TTL_SECONDS
    return session, is_expired

def store_session(session_id: str, activity_data):
    _sessions[session_id] = {
        "activity_data": activity_data,
        "lastFetchedAt": time.time()
    }
