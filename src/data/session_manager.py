import json
import os
from datetime import datetime

class SessionManager:
    SESSIONS_FILE = "sessions.json"

    @staticmethod
    def load_sessions():
        if os.path.exists(SessionManager.SESSIONS_FILE):
            with open(SessionManager.SESSIONS_FILE, "r") as file:
                return json.load(file)
        return {"sessions": []}

    @staticmethod
    def save_sessions(sessions):
        with open(SessionManager.SESSIONS_FILE, "w") as file:
            json.dump(sessions, file, indent=4)

    @staticmethod
    def get_or_create_session(session_id):
        sessions = SessionManager.load_sessions()
        session = next((s for s in sessions["sessions"] if s["id"] == session_id), None)
        if not session:
            session = {"id": session_id, "pairs": []}
            sessions["sessions"].append(session)
            SessionManager.save_sessions(sessions)
        return session

    @staticmethod
    def add_pair(session_id, pair):
        sessions = SessionManager.load_sessions()
        session = next((s for s in sessions["sessions"] if s["id"] == session_id), None)
        if session:
            session["pairs"].append(pair)
        else:
            session = {"id": session_id, "pairs": [pair]}
            sessions["sessions"].append(session)
        SessionManager.save_sessions(sessions)

    @staticmethod
    def update_response(session_id, response):
        sessions = SessionManager.load_sessions()
        session = next((s for s in sessions["sessions"] if s["id"] == session_id), None)
        if session and session["pairs"]:
            session["pairs"][-1]["responseWord"] = response
            SessionManager.save_sessions(sessions)

    @staticmethod
    def load_session(session_id):
        sessions = SessionManager.load_sessions()
        return next((s for s in sessions["sessions"] if s["id"] == session_id), {"id": session_id, "pairs": []})
    
    @staticmethod
    def finalize_session(session_id):
        sessions = SessionManager.load_sessions()
        session = next((s for s in sessions["sessions"] if s["id"] == session_id), None)
        if session:
            session["end_time"] = datetime.now().isoformat()
            SessionManager.save_sessions(sessions)