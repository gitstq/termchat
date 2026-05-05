"""
Main CLI interface for TermChat.

Provides the interactive chat loop with command handling,
multi-session management, and provider switching.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from .config import Config, load_config, save_config, DEFAULT_CONFIG_PATH
from .provider import LLMProvider, Message
from .session import SessionManager
from .ui import TermChatUI


# Command completions
COMMANDS = [
    "/help", "/clear", "/new", "/switch", "/sessions", "/delete",
    "/provider", "/model", "/providers", "/config", "/theme",
    "/save", "/search", "/export", "/test", "/quit", "/exit",
]


class TermChatApp:
    """Main TermChat application."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config = load_config(config_path)
        self.session_manager = SessionManager()
        self.ui = TermChatUI(self.config.theme)
        self._provider: Optional[LLMProvider] = None
        self._running = True
        self._prompt_session: Optional[PromptSession] = None

    def _get_provider(self) -> LLMProvider:
        """Get or create the current LLM provider."""
        provider_config = self.config.get_provider(self.config.default_provider)
        if not provider_config:
            raise ValueError(f"Provider '{self.config.default_provider}' not found")
        return LLMProvider(provider_config)

    def _get_completer(self) -> WordCompleter:
        """Create command completer."""
        return WordCompleter(COMMANDS, ignore_case=True)

    async def _handle_command(self, cmd: str, args: str) -> bool:
        """Handle slash commands. Returns True if should continue loop."""
        cmd = cmd.lower()

        if cmd in ("/quit", "/exit"):
            self._running = False
            return False

        elif cmd == "/help":
            self.ui.print_help()

        elif cmd == "/clear":
            session = self.session_manager.active_session
            if session:
                session.clear_messages()
                self.ui.print_success("Conversation cleared")
            else:
                self.ui.print_warning("No active session")

        elif cmd == "/new":
            if not args:
                self.ui.print_error("Usage: /new <session_name>")
                return True
            try:
                prov_cfg = self.config.get_provider(self.config.default_provider)
                session = self.session_manager.create_session(
                    name=args.strip(),
                    provider=self.config.default_provider,
                    model=prov_cfg.model if prov_cfg else "",
                )
                self.session_manager.set_active(args.strip())
                self.ui.print_success(f"Session '{args.strip()}' created and activated")
            except ValueError as e:
                self.ui.print_error(str(e))

        elif cmd == "/switch":
            if not args:
                self.ui.print_error("Usage: /switch <session_name>")
                return True
            if self.session_manager.set_active(args.strip()):
                self.ui.print_success(f"Switched to session '{args.strip()}'")
            else:
                self.ui.print_error(f"Session '{args.strip()}' not found")

        elif cmd == "/sessions":
            active_name = self.session_manager.active_session.name if self.session_manager.active_session else None
            self.ui.print_sessions(self.session_manager.list_sessions(), active_name)

        elif cmd == "/delete":
            if not args:
                self.ui.print_error("Usage: /delete <session_name>")
                return True
            if self.session_manager.delete_session(args.strip()):
                self.ui.print_success(f"Session '{args.strip()}' deleted")
            else:
                self.ui.print_error(f"Session '{args.strip()}' not found")

        elif cmd == "/provider":
            if not args:
                self.ui.print_error("Usage: /provider <provider_name>")
                return True
            provider_name = args.strip().lower()
            if provider_name in self.config.list_providers():
                self.config.default_provider = provider_name
                save_config(self.config)
                prov_cfg = self.config.get_provider(provider_name)
                self.ui.print_success(
                    f"Switched to provider '{provider_name}' "
                    f"(model: {prov_cfg.model if prov_cfg else 'unknown'})"
                )
            else:
                available = ", ".join(self.config.list_providers())
                self.ui.print_error(f"Unknown provider. Available: {available}")

        elif cmd == "/model":
            if not args:
                self.ui.print_error("Usage: /model <model_name>")
                return True
            prov_cfg = self.config.get_provider(self.config.default_provider)
            if prov_cfg:
                prov_cfg.model = args.strip()
                save_config(self.config)
                self.ui.print_success(f"Model changed to '{args.strip()}'")

        elif cmd == "/providers":
            self.ui.print_providers(self.config.providers, self.config.default_provider)

        elif cmd == "/config":
            prov_cfg = self.config.get_provider(self.config.default_provider)
            config_info = {
                "Default Provider": self.config.default_provider,
                "Model": prov_cfg.model if prov_cfg else "N/A",
                "Theme": self.config.theme,
                "Max History": str(self.config.max_history),
                "Auto Save": str(self.config.auto_save),
                "Stream": str(self.config.stream),
                "Config File": str(DEFAULT_CONFIG_PATH),
                "Sessions Dir": str(self.session_manager.sessions_dir),
            }
            self.ui.print_config(config_info)

        elif cmd == "/theme":
            if not args:
                self.ui.print_error("Usage: /theme <monokai|dark|light>")
                return True
            theme_name = args.strip().lower()
            if theme_name in ("monokai", "dark", "light"):
                self.config.theme = theme_name
                save_config(self.config)
                self.ui = TermChatUI(theme_name)
                self.ui.print_success(f"Theme changed to '{theme_name}'")
            else:
                self.ui.print_error("Available themes: monokai, dark, light")

        elif cmd == "/save":
            session = self.session_manager.active_session
            if session:
                if self.session_manager.save_session(session.name):
                    self.ui.print_success(f"Session '{session.name}' saved")
                else:
                    self.ui.print_error("Failed to save session")
            else:
                self.ui.print_warning("No active session")

        elif cmd == "/search":
            if not args:
                self.ui.print_error("Usage: /search <query>")
                return True
            results = self.session_manager.search_messages(args.strip())
            self.ui.print_search_results(results)

        elif cmd == "/export":
            session = self.session_manager.active_session
            if not session:
                self.ui.print_warning("No active session")
                return True
            export_path = args.strip() or f"{session.name}.md"
            try:
                with open(export_path, "w", encoding="utf-8") as f:
                    f.write(f"# Chat Session: {session.name}\n\n")
                    f.write(f"**Provider:** {session.provider} | **Model:** {session.model}\n\n")
                    f.write("---\n\n")
                    for msg in session.messages:
                        role_label = "**You**" if msg.role == "user" else "**Assistant**"
                        f.write(f"### {role_label}\n\n{msg.content}\n\n---\n\n")
                self.ui.print_success(f"Session exported to {export_path}")
            except IOError as e:
                self.ui.print_error(f"Export failed: {e}")

        elif cmd == "/test":
            try:
                provider = self._get_provider()
                self.ui.print_thinking("Testing connection...")
                success, message = await provider.test_connection()
                if success:
                    self.ui.print_success(message)
                else:
                    self.ui.print_error(message)
                await provider.close()
            except Exception as e:
                self.ui.print_error(f"Test failed: {e}")

        else:
            self.ui.print_error(f"Unknown command: {cmd}. Type /help for available commands.")

        return True

    async def _send_message(self, content: str) -> None:
        """Send a user message and get AI response."""
        session = self.session_manager.active_session
        if not session:
            self.ui.print_warning("No active session. Use /new <name> to create one.")
            return

        # Check provider config
        prov_cfg = self.config.get_provider(self.config.default_provider)
        if not prov_cfg:
            self.ui.print_error(f"Provider '{self.config.default_provider}' not configured")
            return

        # Add user message
        session.add_message("user", content)
        self.ui.print_user_message(content)

        # Get AI response
        try:
            provider = self._get_provider()

            if self.config.stream:
                self.ui.print_stream_start()
                full_response = ""
                async for chunk in provider.chat(
                    session.messages[:-1],  # Exclude the just-added message from history
                    stream=True,
                ):
                    full_response += chunk
                    self.ui.print_stream_chunk(chunk)
                self.ui.print_stream_end()
            else:
                self.ui.print_thinking()
                full_response = ""
                async for chunk in provider.chat(
                    session.messages[:-1],
                    stream=False,
                ):
                    full_response = chunk
                self.ui.print_assistant_message(full_response)

            # Save assistant response
            session.add_message("assistant", full_response)

            # Auto-save
            if self.config.auto_save:
                self.session_manager.save_session(session.name)

            await provider.close()

        except Exception as e:
            self.ui.print_error(f"Failed to get response: {e}")

    async def run(self) -> None:
        """Run the main interactive loop."""
        self.ui.print_banner()

        # Create default session if none exists
        if not self.session_manager.list_sessions():
            prov_cfg = self.config.get_provider(self.config.default_provider)
            default_session = self.session_manager.create_session(
                name="default",
                provider=self.config.default_provider,
                model=prov_cfg.model if prov_cfg else "",
            )
            self.session_manager.set_active("default")

        # Show welcome
        prov_cfg = self.config.get_provider(self.config.default_provider)
        model_name = prov_cfg.model if prov_cfg else "unknown"
        self.ui.print_welcome(self.config.default_provider, model_name)

        # Setup prompt
        self._prompt_session = PromptSession(
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            completer=self._get_completer(),
            multiline=False,
        )

        # Main loop
        while self._running:
            try:
                session_name = ""
                if self.session_manager.active_session:
                    session_name = self.session_manager.active_session.name
                prompt_text = f"[{self.config.default_provider}] {session_name}> "

                user_input = await self._prompt_session.prompt_async(prompt_text)

                if not user_input.strip():
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    parts = user_input.split(None, 1)
                    cmd = parts[0]
                    args = parts[1] if len(parts) > 1 else ""
                    await self._handle_command(cmd, args)
                else:
                    await self._send_message(user_input)

            except KeyboardInterrupt:
                self.ui.print_info("\nUse /quit to exit")
                continue
            except EOFError:
                self._running = False
            except Exception as e:
                self.ui.print_error(f"Unexpected error: {e}")

        # Cleanup
        self.ui.print_info("Goodbye! 👋")


def main():
    """Entry point for the TermChat CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="TermChat - Lightweight universal terminal AI chat assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to configuration file",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create default configuration and exit",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"termchat {__import__('termchat').__version__}",
    )

    args = parser.parse_args()

    if args.init:
        from .config import create_default_config
        config_path = Path(args.config) if args.config else None
        config = create_default_config(config_path)
        print(f"✓ Default configuration created at {config_path or DEFAULT_CONFIG_PATH}")
        print(f"  Edit the file to add your API keys, then run: termchat")
        return

    app = TermChatApp(config_path=Path(args.config) if args.config else None)
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
