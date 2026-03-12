import json
from database.queries import get_session, update_session_transcript

class TranscriptManager:
    """Manages storing, retrieving, and logging manual transcript edits."""

    def get_transcript(self, session_id: str) -> dict:
        session = get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session["session_id"],
            "original_transcript": session["original_transcript"],
            "current_transcript": session["edited_transcript"] if session["edited_transcript"] else session["original_transcript"],
            "version": session["version"]
        }

    def update_transcript(self, session_id: str, new_transcript: str) -> bool:
        """Saves a new edit, incrementing version."""
        # For simplicity, we just store it into the `edited_transcript` table field and bump version.
        update_session_transcript(session_id, new_transcript, is_edited=True, version_increase=1)
        return True
