# shellai — AI Command Generator

Turn natural language into shell commands, right in your terminal.

```bash
ai list all PDF files modified in the last 7 days
ai -p switch to parent directory | iex
ai -c find processes using port 3000 and kill them
```

## Features

| Mode | Flag | Behavior |
|------|------|----------|
| **Interactive** | _(default)_ | Rich panel + `y/n/e` prompt + subprocess execution |
| **Print** | `-p` / `--print` | Print raw command only, pipe to `iex` for in‑shell execution |
| **Clipboard** | `-c` / `--clip` | Print command + copy to clipboard |
| **Setup** | `--setup` | Auto‑configure `$PROFILE` so `ai` runs commands directly in your shell |
| **Teardown** | `--teardown` | Remove the `$PROFILE` configuration |

### The full picture

Before `--setup` — zero configuration, works out of the box:

```bash
ai 列出文件                      # interactive (Rich panel)
ai -p 切换到上级目录 | iex         # pipe mode (cd sticks!)
ai -c 杀掉占用3000端口的进程       # clipboard mode
```

After `--setup` — the best experience, one extra step:

```bash
ai --setup                       # one-time configuration
ai 切换到上级目录                  # runs directly in your shell, no pipe needed!
ai 列出最近7天修改的 PDF 文件       # interactive + subprocess (fallback)
```

You can always override with `.exe`:

```bash
ai.exe 列出文件                   # always goes raw Python, bypasses the PS wrapper
```

## Install

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

### From GitHub

```bash
uv tool install git+https://github.com/alephme/shellai.git
ai --setup     # optionally auto-configure $PROFILE
```

### From source

```bash
git clone https://github.com/alephme/shellai.git
cd shellai
uv tool install -e .
ai --setup
```

## Configuration

Set your API key. Config file takes priority over environment variables.

**Windows (PowerShell):**

```powershell
ni -Force ~/.config/shellai/config.env > $null
@"
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
"@ | Out-File ~/.config/shellai/config.env -Encoding utf8
```

**Linux / macOS:**

```bash
mkdir -p ~/.config/shellai
cat > ~/.config/shellai/config.env << 'EOF'
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
EOF
```

**Supported environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` or `AI_API_KEY` | _(required)_ | Your API key |
| `AI_BASE_URL` | `https://api.deepseek.com/v1` | Any OpenAI‑compatible endpoint |
| `AI_MODEL` | `deepseek-v4-flash` | Model name |

## Usage

### Interactive mode

```bash
ai list all PDF files modified in the last 7 days
ai find processes using port 3000 and kill them
```

Displays the generated command in a Rich syntax‑highlighted panel, then asks:

```
Execute this command? [y/n/e] (y):
```

- `y` — execute (via subprocess, output streamed line‑by‑line)
- `n` — cancel
- `e` — edit the command first, then execute

### Print mode

```bash
ai -p switch to parent directory | iex
ai --print create a new directory called project | iex
```

Prints **only** the raw command to stdout. Pipe to `Invoke-Expression` (`iex`) to execute it in your **current** shell — so `cd`, `Set-Location`, environment variables, and all other side effects actually stick.

### Clipboard mode

```bash
ai -c kill processes using port 3000
ai --clip show network config
```

Prints the command to stdout and copies it to your clipboard. Just Ctrl+V to paste and execute.

### Setup & teardown

```bash
ai --setup      # adds PS wrapper to $PROFILE, copies reload command to clipboard
ai --teardown   # removes PS wrapper from $PROFILE
```

`--setup` writes a one‑line dot‑source command to your PowerShell `$PROFILE`. After a restart, or after pasting the clipboard command in your current shell, `ai` becomes a native shell function:

```bash
ai cd ..        # your working directory actually changes!
ai $env:FOO = 5 # environment variable persists!
```

### When to use which

| Scenario | Best mode |
|----------|-----------|
| I just want to run a command and see output | interactive (default) |
| I need `cd` or env changes to persist | `--setup` + interactive, or `-p \| iex` |
| I want to paste it manually | `-c` |
| I'm scripting | `-p` |
| I'm uninstalling | `--teardown` |

## Architecture

```
PS> ai 列出文件
    │
    ├── (no PS wrapper) → ai.exe 列出文件 → Rich panel + subprocess
    │
    └── (with PS wrapper) → function ai → ai.exe -p 列出文件 → get command text
            └── Invoke-Expression <command>  ← runs in your current shell
```

## Project Structure

```
shellai/
├── pyproject.toml           # metadata, dependencies, entry point
├── .gitignore
└── src/ai_cli/
    ├── __init__.py
    ├── main.py              # CLI logic (5 modes)
    └── shell-ai.ps1         # PowerShell wrapper, auto-installed
```

## License

MIT

---

# shellai — AI 命令行生成器（中文版）

用自然语言生成终端命令。

```bash
ai 列出最近7天修改过的所有 PDF 文件
ai -p 切换到上级目录 | iex
ai -c 找到占用 3000 端口的进程并终止
```

## 功能

| 模式 | 参数 | 行为 |
|------|------|------|
| **交互式** | _(默认)_ | Rich 面板展示 + `y/n/e` 确认 + 子进程执行 |
| **打印** | `-p` / `--print` | 仅输出原始命令，可管道到 `iex` 原地执行 |
| **剪贴板** | `-c` / `--clip` | 打印命令 + 写入剪贴板 |
| **配置** | `--setup` | 自动配置 `$PROFILE`，之后 `ai` 直接原地执行命令 |
| **取消配置** | `--teardown` | 移除 `$PROFILE` 中的配置 |

### 完整使用链路

**不配置 `$PROFILE`（零门槛，装好就能用）：**

```bash
ai 列出文件                      # 交互式（Rich 面板）
ai -p 切换到上级目录 | iex         # 管道模式（cd 真正生效！）
ai -c 杀掉占用3000端口的进程       # 剪贴板模式
```

**配置 `--setup` 后（最佳体验，只需一步）：**

```bash
ai --setup                       # 一次性配置
ai 切换到上级目录                  # 直接原地执行，无需管道！
ai 列出最近7天修改的 PDF 文件       # 交互式 + 子进程执行（回退方案）
```

任何情况下都可以用 `.exe` 后缀绕过 PS 包装函数：

```bash
ai.exe 列出文件                   # 始终走原始 Python，绕过 PS 包装
```

## 安装

### 前提条件

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

### 从 GitHub 安装

```bash
uv tool install git+https://github.com/alephme/shellai.git
ai --setup     # 可选：自动配置 $PROFILE
```

### 从源码安装

```bash
git clone https://github.com/alephme/shellai.git
cd shellai
uv tool install -e .
ai --setup
```

## 配置

通过环境变量或配置文件设置 API Key。配置文件优先级高于环境变量。

**Windows (PowerShell)：**

```powershell
ni -Force ~/.config/shellai/config.env > $null
@"
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
"@ | Out-File ~/.config/shellai/config.env -Encoding utf8
```

**Linux / macOS：**

```bash
mkdir -p ~/.config/shellai
cat > ~/.config/shellai/config.env << 'EOF'
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-v4-flash
EOF
```

**支持的环境变量：**

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENAI_API_KEY` 或 `AI_API_KEY` | _(必填)_ | API 密钥 |
| `AI_BASE_URL` | `https://api.deepseek.com/v1` | 兼容 OpenAI 接口的任意端点 |
| `AI_MODEL` | `deepseek-v4-flash` | 模型名称 |

> 兼容任何 OpenAI 兼容 API（DeepSeek、Ollama 等）。  
> 设置 `AI_BASE_URL` 和 `AI_MODEL` 来切换供应商。

## 用法

### 交互模式

```bash
ai 列出最近7天修改过的所有 PDF 文件
ai 找到占用 3000 端口的进程并终止
```

在 Rich 语法高亮面板中显示生成的命令，然后询问：

```
Execute this command? [y/n/e] (y):
```

- `y` — 执行（子进程，逐行流式输出）
- `n` — 取消
- `e` — 先编辑命令，再执行

### 打印模式

```bash
ai -p 切换到上级目录 | iex
ai --print 创建一个叫 project 的新目录 | iex
```

**仅**输出原始命令文本到 stdout。管道到 `Invoke-Expression`（`iex`）即可在**当前** shell 中执行——`cd`、`Set-Location`、环境变量等所有副作用都会保留。

### 剪贴板模式

```bash
ai -c 找到占用 3000 端口的进程并终止
ai --clip 显示网络配置
```

打印命令并写入剪贴板。直接 Ctrl+V 粘贴即可执行。

### 配置与取消

```bash
ai --setup      # 写入 PS 包装函数到 $PROFILE，同时复制重载命令到剪贴板
ai --teardown   # 从 $PROFILE 中移除 PS 包装函数
```

`--setup` 会往你的 PowerShell `$PROFILE` 末尾追加一行 dot‑source 命令。重启终端或粘贴剪贴板上的命令后，`ai` 就会变成原生 shell 函数：

```bash
ai cd ..        # 工作目录真的变了！
ai $env:FOO = 5 # 环境变量持久生效！
```

### 模式选择指南

| 场景 | 推荐模式 |
|------|-----------|
| 只想运行命令看看输出 | 交互式（默认） |
| 需要 `cd` 或环境变量持久生效 | `--setup` + 交互式，或 `-p \| iex` |
| 想手动粘贴命令 | `-c` |
| 在脚本中使用 | `-p` |
| 卸载 | `--teardown` |

## 架构

```
PS> ai 列出文件
    │
    ├── (无 PS 包装) → ai.exe 列出文件 → Rich 面板 + 子进程执行
    │
    └── (有 PS 包装) → function ai → ai.exe -p 列出文件 → 获取命令文本
            └── Invoke-Expression <命令>  ← 在当前 shell 中执行
```

## 项目结构

```
shellai/
├── pyproject.toml           # 元数据、依赖、入口点
├── .gitignore
└── src/ai_cli/
    ├── __init__.py
    ├── main.py              # CLI 逻辑（5 种模式）
    └── shell-ai.ps1         # PowerShell 包装函数，随包安装
```

## 许可证

MIT
