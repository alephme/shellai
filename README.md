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

---

## shellai — AI 命令行生成器（中文版）

用自然语言生成终端命令，直接在终端里用。

```bash
ai 列出最近7天修改过的所有 PDF 文件
ai -p 切换到上级目录 | iex
ai -c 找到占用 3000 端口的进程并终止
```

### 功能

| 模式 | 短选项 | 长选项 | 行为 |
|------|--------|--------|------|
| **交互式** | _(默认)_ | _(默认)_ | Rich 面板展示 + `y/n/e` 确认 + 子进程执行 |
| **打印** | `-p` | `--print` | 仅输出原始命令，管道到 `iex` 原地执行 |
| **剪贴板** | `-c` | `--clip` | 打印命令 + 写入剪贴板 |
| **配置** | — | `--setup` | 自动配置 `$PROFILE`，之后 `ai` 直接原地执行 |
| **取消配置** | — | `--teardown` | 移除 `$PROFILE` 中的配置 |

### 安装

```bash
git clone https://github.com/alephme/shellai.git
cd shellai
uv tool install .
ai --setup     # 可选：一键配置 $PROFILE
```

### 配置

配置文件优先级高于环境变量。

**配置文件** (`~/.config/shellai/config.env`)：

```bash
OPENAI_API_KEY=sk-xxx
AI_BASE_URL=https://api.deepseek.com
AI_MODEL=deepseek-v4-flash
```

**或通过环境变量：**

| 变量 | 默认值 | 说明 |
|----------|---------|------|
| `OPENAI_API_KEY` / `AI_API_KEY` | _(必填)_ | API 密钥 |
| `AI_BASE_URL` | `https://api.deepseek.com/v1` | OpenAI 兼容接口地址 |
| `AI_MODEL` | `deepseek-v4-flash` | 模型名称 |

> 兼容任何 OpenAI 兼容 API（DeepSeek、Ollama 等）。

### 用法

#### 交互模式

```bash
ai 列出最近7天修改过的所有 PDF 文件
```

在 Rich 语法高亮面板中显示生成的命令，然后 `y/n/e` 选择。

#### 打印 / 管道模式

```bash
ai -p 切换到上级目录 | iex
ai --print 创建一个叫 project 的新目录 | iex
```

**仅**输出原始命令文本到 stdout。管道到 `Invoke-Expression`（`iex`）即可在**当前** shell 中执行——`cd` 和环境变量修改都会保留。

#### 剪贴板模式

```bash
ai -c 找到占用 3000 端口的进程并终止
ai --clip 显示网络配置
```

打印命令**同时**复制到剪贴板。

#### 配置与取消

```bash
ai --setup      # 往 $PROFILE 添加 PS 包装函数
ai --teardown   # 从 $PROFILE 中移除 PS 包装函数
```

执行 `--setup` 后（重启终端或重新加载），`ai` 直接在当前 shell 中运行：

```bash
ai cd ..        # 工作目录真的变了
```

### 许可证

MIT
