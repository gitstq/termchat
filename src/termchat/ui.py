"""
Terminal UI rendering for TermChat.

Uses Rich library for beautiful terminal output with Markdown rendering,
syntax highlighting, and themed display.
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich.theme import Theme
from rich import box
from typing import Optional, List, Dict, Any

from . import __version__

# Custom theme for TermChat
TERMCHAT_THEME = Theme({
    "title": "bold cyan",
    "subtitle": "dim cyan",
    "user_msg": "bold green",
    "assistant_msg": "bold blue",
    "system_msg": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "info": "bold cyan",
    "warning": "bold yellow",
    "dim": "dim",
    "prompt": "bold magenta",
    "border": "cyan",
    "help_key": "bold yellow",
    "help_desc": "white",
})

# Built-in themes
THEMES = {
    "monokai": TERMCHAT_THEME,
    "dark": Theme({
        "title": "bold white",
        "subtitle": "dim white",
        "user_msg": "bold bright_green",
        "assistant_msg": "bold bright_blue",
        "system_msg": "bold bright_yellow",
        "error": "bold bright_red",
        "success": "bold bright_green",
        "info": "bold bright_cyan",
        "warning": "bold bright_yellow",
        "dim": "dim",
        "prompt": "bold bright_magenta",
        "border": "bright_cyan",
        "help_key": "bold bright_yellow",
        "help_desc": "white",
    }),
    "light": Theme({
        "title": "bold black",
        "subtitle": "dim black",
        "user_msg": "bold green4",
        "assistant_msg": "bold blue",
        "system_msg": "bold dark_orange",
        "error": "bold red",
        "success": "bold green4",
        "info": "bold deep_sky_blue4",
        "warning": "bold dark_orange",
        "dim": "grey50",
        "prompt": "bold medium_purple4",
        "border": "deep_sky_blue4",
        "help_key": "bold dark_orange",
        "help_desc": "black",
    }),
}


class TermChatUI:
    """Terminal UI renderer for TermChat."""

    def __init__(self, theme_name: str = "monokai"):
        self.theme_name = theme_name
        theme = THEMES.get(theme_name, TERMCHAT_THEME)
        self.console = Console(theme=theme)
        self._streaming_content = ""

    def print_banner(self) -> None:
        """Print the application banner."""
        banner = Text()
        banner.append("╔══════════════════════════════════════╗\n", style="border")
        banner.append("║", style="border")
        banner.append("          🤖 TermChat ", style="title")
        banner.append("              ║\n", style="border")
        banner.append("║", style="border")
        banner.append(f"    v{__version__} · Terminal AI Chat  ", style="subtitle")
        banner.append("  ║\n", style="border")
        banner.append("╚══════════════════════════════════════╝", style="border")
        self.console.print(banner)

    def print_welcome(self, provider: str, model: str) -> None:
        """Print welcome message with current provider info."""
        self.console.print()
        self.console.print(
            Panel(
                f"[info]Provider:[/info] {provider}\n"
                f"[info]Model:[/info] {model}\n"
                f"[dim]Type /help for available commands[/dim]",
                title="🚀 TermChat Ready",
                border_style="border",
                box=box.ROUNDED,
            )
        )

    def print_user_message(self, content: str) -> None:
        """Print a user message."""
        self.console.print()
        self.console.print(f"[user_msg]│ You:[/user_msg]")
        self.console.print(Panel(content, border_style="green", box=box.ROUNDED, padding=(0, 1)))

    def print_assistant_message(self, content: str) -> None:
        """Print an assistant message with Markdown rendering."""
        self.console.print()
        self.console.print("[assistant_msg]│ Assistant:[/assistant_msg]")
        try:
            md = Markdown(content)
            self.console.print(Panel(md, border_style="blue", box=box.ROUNDED, padding=(0, 1)))
        except Exception:
            self.console.print(Panel(content, border_style="blue", box=box.ROUNDED, padding=(0, 1)))

    def print_stream_start(self) -> None:
        """Mark the beginning of a streaming response."""
        self.console.print()
        self.console.print("[assistant_msg]│ Assistant:[/assistant_msg]")
        self._streaming_content = ""

    def print_stream_chunk(self, chunk: str) -> None:
        """Print a streaming chunk (accumulates for final render)."""
        self._streaming_content += chunk
        # Show a simple spinner-like indicator
        self.console.print(chunk, end="", highlight=False)

    def print_stream_end(self) -> None:
        """Finalize streaming output."""
        self.console.print()  # newline after streaming

    def print_system_message(self, content: str) -> None:
        """Print a system message."""
        self.console.print(f"[system_msg]⚡ System:[/system_msg] {content}")

    def print_error(self, message: str) -> None:
        """Print an error message."""
        self.console.print(f"[error]✗ Error:[/error] {message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        self.console.print(f"[success]✓[/success] {message}")

    def print_info(self, message: str) -> None:
        """Print an info message."""
        self.console.print(f"[info]ℹ[/info] {message}")

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        self.console.print(f"[warning]⚠[/warning] {message}")

    def print_help(self) -> None:
        """Print help information."""
        table = Table(
            title="📖 Available Commands",
            border_style="border",
            box=box.ROUNDED,
            show_header=True,
            header_style="title",
        )
        table.add_column("Command", style="help_key", width=22)
        table.add_column("Description", style="help_desc")

        commands = [
            ("/help", "Show this help message"),
            ("/clear", "Clear current conversation"),
            ("/new <name>", "Create a new session"),
            ("/switch <name>", "Switch to another session"),
            ("/sessions", "List all sessions"),
            ("/delete <name>", "Delete a session"),
            ("/provider <name>", "Switch LLM provider"),
            ("/model <name>", "Change model for current provider"),
            ("/providers", "List available providers"),
            ("/config", "Show current configuration"),
            ("/theme <name>", "Change UI theme (monokai/dark/light)"),
            ("/save", "Save current session"),
            ("/search <query>", "Search messages across all sessions"),
            ("/export <path>", "Export current session to Markdown file"),
            ("/test", "Test connection to current provider"),
            ("/quit", "Exit TermChat"),
        ]
        for cmd, desc in commands:
            table.add_row(cmd, desc)

        self.console.print(table)

    def print_sessions(self, sessions: list, active_name: Optional[str] = None) -> None:
        """Print session list."""
        if not sessions:
            self.console.print("[dim]No sessions found. Use /new <name> to create one.[/dim]")
            return

        table = Table(
            title="📋 Sessions",
            border_style="border",
            box=box.ROUNDED,
            show_header=True,
            header_style="title",
        )
        table.add_column("Name", style="info", width=20)
        table.add_column("Provider", width=12)
        table.add_column("Model", width=25)
        table.add_column("Messages", justify="right", width=8)
        table.add_column("Updated", style="dim", width=20)
        table.add_column("Active", justify="center", width=6)

        for s in sessions:
            is_active = "✓" if s.name == active_name else ""
            table.add_row(
                s.name,
                s.provider,
                s.model or "-",
                str(s.message_count),
                s.updated_at[:19],
                is_active,
            )

        self.console.print(table)

    def print_providers(self, providers: Dict[str, Any], current: str) -> None:
        """Print provider list."""
        table = Table(
            title="🔌 Providers",
            border_style="border",
            box=box.ROUNDED,
            show_header=True,
            header_style="title",
        )
        table.add_column("Name", style="info", width=14)
        table.add_column("Base URL", width=45)
        table.add_column("Model", width=35)
        table.add_column("API Key", width=20)
        table.add_column("Active", justify="center", width=6)

        for name, prov in providers.items():
            is_active = "✓" if name == current else ""
            key_status = "✓ Set" if prov.api_key else "✗ Missing"
            key_style = "success" if prov.api_key else "error"
            table.add_row(
                name,
                prov.base_url,
                prov.model,
                f"[{key_style}]{key_status}[/{key_style}]",
                is_active,
            )

        self.console.print(table)

    def print_config(self, config_dict: Dict[str, Any]) -> None:
        """Print current configuration."""
        self.console.print(
            Panel(
                "\n".join(f"[info]{k}:[/info] {v}" for k, v in config_dict.items()),
                title="⚙️ Configuration",
                border_style="border",
                box=box.ROUNDED,
            )
        )

    def print_search_results(self, results: List[Dict[str, Any]]) -> None:
        """Print search results."""
        if not results:
            self.console.print("[dim]No results found.[/dim]")
            return

        self.console.print(f"[info]Found {len(results)} results:[/info]\n")
        for i, r in enumerate(results[:10], 1):
            role_style = "user_msg" if r["role"] == "user" else "assistant_msg"
            self.console.print(
                f"[dim][{i}][/dim] [{role_style}]{r['role']}[/{role_style}] "
                f"in [info]{r['session']}[/info]: "
                f"{r['content'][:100]}..."
            )

    def print_thinking(self, message: str = "Thinking...") -> None:
        """Print a thinking indicator."""
        self.console.print(f"[dim]💭 {message}[/dim]")

    def clear(self) -> None:
        """Clear the terminal."""
        self.console.clear()
