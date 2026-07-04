# shellai — AI Command Generator

Turn natural language into shell commands, right in your terminal.

```
ai list all PDF files modified in the last 7 days
ai -p find node_modules folders | iex
ai -c kill processes using port 3000
```

## Features

- **Interactive mode** — AI generates a command, shows it in a Rich panel, asks `y/n/e`
- **Pipe mode** (`-p`) — print-only, pipe to `iex` to execute in your current shell
- **Clipboard mode** (`-c`) — print + automatically copy to clipboard
- **One‑click setup** (`--setup`) — configure `$PROFILE` for in‑shell execution
- **One‑click teardown** (`--teardown`) — remove the configuration

## Install

```bash
# Prerequisite: Python 3.10+, uv
uv tool install git+https://github.com/alephpi/shellai.git
```

Or from source:

```bash
git clone https://github.com/alephpi/shellai.git
cd shellai
uv tool install -e .
```

## Configuration

Set your API key via environment variable or config file:

```bash
# Option 1: environment variable
export OPENAI_API_KEY=sk-xxx

# Option 2: config file
mkdir -p ~/.config/shellai
cat > ~/.config/shellai/config.env << 'EOF'
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
EOF
```

> Compatible with any OpenAI‑compatible API (DeepSeek, Ollama, etc.).  
> Set `AI_BASE_URL` and `AI_MODEL` to switch providers.

## Usage

### Interactive mode (subprocess execution)

```bash
ai list all PDF files modified in the last 7 days
ai find processes using port 3000 and kill them
```

Displays a Rich panel with the generated command, then asks `y/n/e`.

### Pipe mode — execute in current shell

```bash
ai -p switch to parent directory | iex
ai -p create a new directory called temp | iex
```

Prints the raw command to stdout — pipe to `Invoke-Expression` (`iex`) to run it in your **current** shell session, so `cd` and environment changes stick.

### Clipboard mode

```bash
ai -c kill processes using port 3000
```

Prints the command and copies it to your clipboard — just Ctrl+V to execute.

### One‑click setup (recommended)

```bash
ai --setup
```

Adds a `ai` wrapper function to `$PROFILE`. After that:

```bash
ai switch to parent directory   # cd works!
```

To remove:

```bash
ai --teardown
```

## Project Structure

```
shellai/
├── pyproject.toml           # Project metadata + entry point
└── src/ai_cli/
    ├── __init__.py
    ├── main.py              # CLI logic
    └── shell-ai.ps1         # PowerShell wrapper for in‑shell execution
```

## License

MIT
