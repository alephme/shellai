"""
ai — AI-powered CLI command generator and executor.

Usage:
    ai <natural language prompt>             # interactive mode (Rich panel, subprocess)
    ai -p <prompt>                           # print-only (for pipe: ai -p ... | iex)
    ai -c <prompt>                           # print + copy to clipboard
    ai --setup                               # auto-configure $PROFILE for in-shell execution
    ai --teardown                            # remove $PROFILE configuration

Examples:
    ai list all PDF files modified in the last 7 days
    ai -p find node_modules folders | iex
    ai -c kill processes using port 3000
"""

import base64
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.markdown import Markdown

console = Console()

# ---------------------------------------------------------------------------
# Configuration — loaded immediately at import time
# ---------------------------------------------------------------------------

CONFIG_FILE = Path.home() / ".config" / "shellai" / "config.env"
load_dotenv(CONFIG_FILE, override=True)

API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("AI_API_KEY")
BASE_URL = os.environ.get("AI_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.environ.get("AI_MODEL", "deepseek-v4-flash")

# Path to the bundled shell-ai.ps1 (installed alongside this module)
_THIS_DIR = Path(__file__).resolve().parent
_PS1_PATH = _THIS_DIR / "shell-ai.ps1"


# ---------------------------------------------------------------------------
# Help text
# ---------------------------------------------------------------------------

HELP_TEXT = Markdown("""\
# ai — AI Command Generator

**Usage:** `ai <natural language description>`

**Modes:**
- `ai <prompt>` — interactive mode (Rich panel + subprocess execution)
- `ai -p <prompt>` — print-only, for piping: `ai -p ... | iex`
- `ai -c <prompt>` — print + copy to clipboard
- `ai --setup` — configure `$PROFILE` for in-shell execution
- `ai --teardown` — remove `$PROFILE` configuration

**Examples:**
```
ai list all PDF files modified in the last 7 days
ai -p switch to parent directory | iex
ai -c find processes using port 3000 and kill them
```

**Configuration (environment variables):**
- `OPENAI_API_KEY` or `AI_API_KEY` — your API key *(required)*
- `AI_BASE_URL` — API base URL (default: `https://api.deepseek.com/v1`)
- `AI_MODEL` — model name (default: `deepseek-v4-flash`)

You can also place these in `~/.config/shellai/config.env`:
```
OPENAI_API_KEY=sk-xxxxxxxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
```
""")


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def build_system_prompt() -> str:
    """Build the system prompt instructing the LLM how to generate commands."""
    shell = os.environ.get("SHELL", "powershell")
    os_name = sys.platform

    return f"""You are a command-line expert. Your ONLY job is to generate a single shell command that
fulfills the user's request. Follow these rules STRICTLY:

- Output ONLY the raw command text — no markdown fences, no explanations, no extra words.
- The command must be valid for: {shell} on {os_name}.
- Use full paths when sensible; avoid destructive operations unless explicitly requested.
- Prefer PowerShell-native cmdlets over aliases (e.g., Get-ChildItem instead of ls, Select-String instead of grep).
- If the request is ambiguous, generate the safest reasonable interpretation.
- Keep the command as a single pipeline or one-liner when possible.
- NEVER include ``` or any formatting — output the command as raw text only."""


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def generate_command(prompt: str) -> str:
    """Call the LLM and return the generated command string."""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    command = response.choices[0].message.content.strip()
    return command


# ---------------------------------------------------------------------------
# Display (interactive mode)
# ---------------------------------------------------------------------------

def display_command(command: str) -> None:
    """Display the generated command in a syntax-highlighted panel."""
    console.print()
    console.print(
        Panel(
            Syntax(command, "powershell", theme="monokai", word_wrap=True),
            title="[bold yellow]Generated Command[/bold yellow]",
            border_style="yellow",
        )
    )


def confirm_execution() -> str:
    """Ask the user what to do. Returns 'y', 'n', or 'e'."""
    console.print()
    choice = Prompt.ask(
        "[bold]Execute this command?[/bold]",
        choices=["y", "n", "e"],
        default="y",
        show_choices=True,
    )
    return choice


def edit_command(command: str) -> str:
    """Let the user edit the command before executing."""
    console.print()
    console.print("[dim]Edit the command below. Press Enter when done.[/dim]")
    console.print()
    new_command = Prompt.ask("Command", default=command)
    return new_command.strip()


# ---------------------------------------------------------------------------
# Execution (interactive mode — subprocess)
# ---------------------------------------------------------------------------

def run_command(command: str) -> None:
    """Execute the command via subprocess and stream output."""
    console.print()
    console.rule("[bold green]Executing[/bold green]")
    console.print(f"[dim]$ {command}[/dim]")
    console.print()

    try:
        if sys.platform == "win32":
            shell_cmd = ["powershell", "-NoProfile", "-Command", command]
        else:
            shell_cmd = [os.environ.get("SHELL", "/bin/sh"), "-c", command]

        process = subprocess.Popen(
            shell_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout:
            for line in process.stdout:
                console.print(line, end="")

        process.wait()

        console.print()
        if process.returncode == 0:
            console.rule("[bold green]✓ Done[/bold green]")
        else:
            console.rule(f"[bold red]✗ Exit code: {process.returncode}[/bold red]")

    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] Shell not found.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# ---------------------------------------------------------------------------
# Clipboard
# ---------------------------------------------------------------------------

def copy_to_clipboard(text: str) -> None:
    """Copy *text* to the Windows clipboard via PowerShell Set-Clipboard."""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
            input=text,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        console.print("[bold red]Error:[/bold red] Failed to copy to clipboard.")


# ---------------------------------------------------------------------------
# $PROFILE management
# ---------------------------------------------------------------------------

def _get_profile_path() -> Path:
    """Return the PowerShell profile path (e.g. $PROFILE)."""
    profile = os.environ.get("PROFILE", "")
    if not profile:
        home = Path.home()
        pwsh_dir = home / "Documents" / "PowerShell"
        if pwsh_dir.exists():
            profile = str(pwsh_dir / "Microsoft.PowerShell_profile.ps1")
        else:
            profile = str(home / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1")
    return Path(profile)


def _setup_source_line() -> str:
    """Return the dot-source line to add to $PROFILE."""
    return f'. "{_PS1_PATH}"  # ai CLI wrapper\n'


def setup_profile() -> None:
    """Add ai wrapper to $PROFILE if not already present."""
    profile_path = _get_profile_path()
    line = _setup_source_line()

    profile_path.parent.mkdir(parents=True, exist_ok=True)

    if profile_path.exists():
        content = profile_path.read_text(encoding="utf-8")
        if line in content:
            console.print("[bold green]OK:[/bold green] Already configured in $PROFILE.")
            return
    else:
        content = ""

    with open(profile_path, "a", encoding="utf-8") as f:
        f.write(line)

    cmd = f'. "{_PS1_PATH}"'
    copy_to_clipboard(cmd)
    console.print(
        f"[bold green]Done:[/bold green] Added to [bold]{profile_path}[/bold]\n"
        f"   Next time you open a shell, [bold]ai[/bold] will run commands in-session.\n"
        f"   Loading command copied to clipboard: [bold]{cmd}[/bold]"
    )


def teardown_profile() -> None:
    """Remove ai wrapper lines from $PROFILE."""
    profile_path = _get_profile_path()

    if not profile_path.exists():
        console.print("[bold green]OK:[/bold green] No $PROFILE found, nothing to remove.")
        return

    content = profile_path.read_text(encoding="utf-8")
    new_lines = []
    removed = 0
    for line in content.splitlines(keepends=True):
        if "shell-ai.ps1" in line:
            removed += 1
            continue
        new_lines.append(line)

    if removed == 0:
        console.print("[bold green]OK:[/bold green] No ai configuration found in $PROFILE.")
        return

    profile_path.write_text("".join(new_lines), encoding="utf-8")
    console.print(
        f"[bold green]Done:[/bold green] Removed {removed} line(s) from [bold]{profile_path}[/bold]."
    )


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

OPTS_ABBREV = {"-p": "print", "-c": "clip"}
OPTS_LONG = {"--print": "print", "--clip": "clip", "--setup": "setup", "--teardown": "teardown"}


def parse_args() -> tuple[str, str | None]:
    """Parse sys.argv. Returns (mode, prompt).

    mode is one of: "help", "print", "clip", "setup", "teardown", "interactive"
    """
    if len(sys.argv) < 2:
        return ("help", None)

    first = sys.argv[1]

    if first in OPTS_ABBREV:
        mode = OPTS_ABBREV[first]
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        return (mode, prompt)

    if first in OPTS_LONG:
        mode = OPTS_LONG[first]
        if mode in ("setup", "teardown"):
            return (mode, None)
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        return (mode, prompt)

    return ("interactive", " ".join(sys.argv[1:]))


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the `ai` CLI command."""
    mode, prompt = parse_args()

    # ---- help ----
    if mode == "help":
        console.print(HELP_TEXT)
        return

    # ---- setup / teardown (no API key needed) ----
    if mode == "setup":
        setup_profile()
        return
    if mode == "teardown":
        teardown_profile()
        return

    # ---- all other modes need an API key ----
    if not API_KEY:
        console.print(
            "[bold red]Error:[/bold red] No API key found.\n"
            "Set [bold]OPENAI_API_KEY[/bold] or [bold]AI_API_KEY[/bold] environment variable,\n"
            "or create [bold]~/.config/shellai/config.env[/bold] with your credentials."
        )
        sys.exit(1)

    # ---- print / clip modes ----
    if mode in ("print", "clip"):
        if not prompt:
            console.print(f"[bold red]Error:[/bold red] -{mode[0]} requires a prompt.")
            sys.exit(1)
        try:
            command = generate_command(prompt)
        except Exception as e:
            console.print(f"[bold red]API Error:[/bold red] {e}")
            sys.exit(1)
        print(command)
        if mode == "clip":
            copy_to_clipboard(command)
            print("(Copied to clipboard)", file=sys.stderr)
        return

    # ---- interactive mode (default) ----
    if not prompt:
        console.print(HELP_TEXT)
        return

    with console.status("[bold cyan]Generating command...[/bold cyan]", spinner="dots"):
        try:
            command = generate_command(prompt)
        except Exception as e:
            console.print(f"[bold red]API Error:[/bold red] {e}")
            sys.exit(1)

    display_command(command)

    while True:
        choice = confirm_execution()
        if choice == "y":
            run_command(command)
            break
        elif choice == "n":
            console.print("[dim]Cancelled.[/dim]")
            break
        elif choice == "e":
            command = edit_command(command)
            display_command(command)


if __name__ == "__main__":
    main()
