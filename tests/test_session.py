"""Tests for TermChat session management module."""

import json
import tempfile
from pathlib import Path

import pytest

from termchat.session import Session, SessionManager
from termchat.provider import Message


class TestSession:
    """Tests for Session class."""

    def test_create_session(self):
        session = Session(name="test-session", provider="openai", model="gpt-4")
        assert session.name == "test-session"
        assert session.provider == "openai"
        assert session.model == "gpt-4"
        assert session.message_count == 0
        assert session.created_at is not None

    def test_add_message(self):
        session = Session(name="test")
        session.add_message("user", "Hello")
        session.add_message("assistant", "Hi there!")
        assert session.message_count == 2
        assert session.messages[0].role == "user"
        assert session.messages[1].content == "Hi there!"

    def test_clear_messages(self):
        session = Session(name="test")
        session.add_message("user", "Hello")
        session.clear_messages()
        assert session.message_count == 0

    def test_to_dict(self):
        session = Session(name="test", provider="deepseek", model="deepseek-chat")
        session.add_message("user", "Hello")
        data = session.to_dict()
        assert data["name"] == "test"
        assert data["provider"] == "deepseek"
        assert len(data["messages"]) == 1

    def test_from_dict(self):
        data = {
            "name": "test",
            "provider": "ollama",
            "model": "llama3",
            "created_at": "2024-01-01T00:00:00",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi!"},
            ],
        }
        session = Session.from_dict(data)
        assert session.name == "test"
        assert session.provider == "ollama"
        assert session.message_count == 2


class TestSessionManager:
    """Tests for SessionManager class."""

    def test_create_and_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("s1", "openai", "gpt-4")
            manager.create_session("s2", "deepseek", "deepseek-chat")
            sessions = manager.list_sessions()
            assert len(sessions) == 2

    def test_create_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("s1")
            with pytest.raises(ValueError):
                manager.create_session("s1")

    def test_delete_session(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("s1")
            assert manager.delete_session("s1") is True
            assert len(manager.list_sessions()) == 0

    def test_delete_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            assert manager.delete_session("nonexistent") is False

    def test_set_active(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("s1")
            manager.create_session("s2")
            assert manager.set_active("s1") is True
            assert manager.active_session.name == "s1"
            assert manager.set_active("s2") is True
            assert manager.active_session.name == "s2"

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create and save
            manager1 = SessionManager(Path(tmpdir))
            manager1.create_session("persist-test", "openai", "gpt-4")
            manager1.get_session("persist-test").add_message("user", "Hello")
            manager1.save_session("persist-test")

            # Reload
            manager2 = SessionManager(Path(tmpdir))
            session = manager2.get_session("persist-test")
            assert session is not None
            assert session.message_count == 1
            assert session.messages[0].content == "Hello"

    def test_search_messages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("s1")
            manager.get_session("s1").add_message("user", "I love Python programming")
            manager.get_session("s1").add_message("assistant", "Python is great!")

            results = manager.search_messages("Python")
            assert len(results) == 2

            results = manager.search_messages("Java")
            assert len(results) == 0

    def test_special_characters_in_name(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = SessionManager(Path(tmpdir))
            manager.create_session("test session (1)")
            session = manager.get_session("test session (1)")
            assert session is not None
