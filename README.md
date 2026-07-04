# shellai — AI Command Generator

Turn natural language into shell commands, right in your terminal.

```bash
ai list all PDF files modified in the last 7 days
ai -p switch to parent directory | iex
ai -c find processes using port 3000 and kill them
```

## Features

| Mode | Short | Long | Behavior |
|------|-------|------|----------|
| **Interactive** | _(default)_ | _(default)_ | Rich panel + `y/n/e` + subprocess execution |
| **Print** | `-p` | `--print` | Raw command to stdout, pipe to `iex` for in‑shell execution |
| **Clipboard** | `-c` | `--clip` | Print command + copy to clipboard |
| **Setup** | — | `--setup` | Auto‑configure `$PROFILE` for in‑shell execution |
| **Teardown** | — | `--teardown` | Remove `$PROFILE` configuration |

## Install

```bash
git clone https://github.com/alephme/shellai.git
cd shellai
uv tool install .
ai --setup     # optional: auto-configure $PROFILE
```

## Configuration

Config file takes priority over environment variables.

**Config file** (`~/.config/shellai/config.env`):

```bash
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com
AI_MODEL=deepseek-v4-flash
```

**Or environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` / `AI_API_KEY` | _(required)_ | API key |
| `AI_BASE_URL` | `https://api.deepseek.com/v1` | OpenAI‑compatible endpoint |
| `AI_MODEL` | `deepseek-v4-flash` | Model name |

> Works with any OpenAI‑compatible API (DeepSeek, Ollama, etc.).

## Usage

### Interactive mode

```bash
ai list all PDF files modified in the last 7 days
```

Displays the command in a Rich syntax‑highlighted panel, then `y/n/e`.

### Print / pipe mode

```bash
ai -p switch to parent directory | iex
ai --print create a new directory called project | iex
```

Prints **only** the raw command. Pipe to `Invoke-Expression` (`iex`) to run it in your **current** shell — `cd` and env changes stick.

### Clipboard mode

```bash
ai -c kill processes using port 3000
ai --clip show network config
```

Prints the command **and** copies it to clipboard.

### Setup & teardown

```bash
ai --setup      # add PS wrapper to $PROFILE
ai --teardown   # remove PS wrapper from $PROFILE
```

After `--setup` (and restart / re‑sourcing), `ai` runs directly in your shell:

```bash
ai cd ..        # working directory actually changes
```

## License

MIT
