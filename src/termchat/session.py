"""
Session management for TermChat.

Handles creating, loading, saving, and switching between chat sessions.
Sessions are persisted as JSON files on disk.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from .provider import Message


class Session:
    """Represents a single chat session with message history."""

    def __init__(
        self,
        name: str,
        provider: str = "openai",
        model: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.name = name
        self.provider = provider
        self.model = model
        self.messages: List[Message] = []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        self.messages.append(Message(role, content))
        self.updated_at = datetime.now().isoformat()

    def get_messages(self) -> List[Message]:
        """Get all messages in the session."""
        return self.messages

    def clear_messages(self) -> None:
        """Clear all messages."""
        self.messages.clear()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize session to dictionary."""
        return {
            "name": self.name,
            "provider": self.provider,
            "model": self.model,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "messages": [{"role": m.role, "content": m.content} for m in self.messages],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Deserialize session from dictionary."""
        session = cls(
            name=data["name"],
            provider=data.get("provider", "openai"),
            model=data.get("model", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
        for msg_data in data.get("messages", []):
            session.messages.append(Message(msg_data["role"], msg_data["content"]))
        return session

    @property
    def message_count(self) -> int:
        """Return the number of messages."""
        return len(self.messages)


class SessionManager:
    """Manages multiple chat sessions with disk persistence."""

    def __init__(self, sessions_dir: Optional[Path] = None):
        self.sessions_dir = sessions_dir or Path.home() / ".termchat" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[str, Session] = {}
        self._active_session: Optional[Session] = None
        self._load_all_sessions()

    def _session_path(self, name: str) -> Path:
        """Get the file path for a session."""
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        return self.sessions_dir / f"{safe_name}.json"

    def _load_all_sessions(self) -> None:
        """Load all sessions from disk."""
        for path in self.sessions_dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                session = Session.from_dict(data)
                self._sessions[session.name] = session
            except (json.JSONDecodeError, KeyError, IOError):
                continue

    def create_session(self, name: str, provider: str = "openai", model: str = "") -> Session:
        """Create a new session."""
        if name in self._sessions:
            raise ValueError(f"Session '{name}' already exists")
        session = Session(name=name, provider=provider, model=model)
        self._sessions[name] = session
        self.save_session(name)
        return session

    def get_session(self, name: str) -> Optional[Session]:
        """Get a session by name."""
        return self._sessions.get(name)

    def delete_session(self, name: str) -> bool:
        """Delete a session."""
        if name not in self._sessions:
            return False
        path = self._session_path(name)
        if path.exists():
            path.unlink()
        del self._sessions[name]
        if self._active_session and self._active_session.name == name:
            self._active_session = None
        return True

    def list_sessions(self) -> List[Session]:
        """List all sessions sorted by updated_at."""
        return sorted(
            self._sessions.values(),
            key=lambda s: s.updated_at,
            reverse=True,
        )

    def save_session(self, name: str) -> bool:
        """Save a session to disk."""
        session = self._sessions.get(name)
        if not session:
            return False
        path = self._session_path(name)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    @property
    def active_session(self) -> Optional[Session]:
        """Get the currently active session."""
        return self._active_session

    def set_active(self, name: str) -> bool:
        """Set the active session."""
        if name not in self._sessions:
            return False
        self._active_session = self._sessions[name]
        return True

    def search_messages(self, query: str) -> List[Dict[str, Any]]:
        """Search across all sessions for messages containing the query."""
        results = []
        query_lower = query.lower()
        for session in self._sessions.values():
            for msg in session.messages:
                if query_lower in msg.content.lower():
                    results.append({
                        "session": session.name,
                        "role": msg.role,
                        "content": msg.content[:200],
                        "full_content": msg.content,
                    })
        return results
