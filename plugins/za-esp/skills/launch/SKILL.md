---
name: launch
description: "在新终端窗口中启动 claude-esp，实时展示 Claude Code 的思考过程。当用户说'显示思考过程'、'打开思考流程'、'启动 esp'、'开启实时思考'、'show thinking'、'launch esp'、'新窗口打开 esp'、'打开esp'、'打开 esp'、'开启esp'、'开启 esp' 时触发。"
version: 0.4.4
allowed-tools:
  - Bash
---

# launch — 在新终端中启动 claude-esp

自动定位 claude-esp 二进制文件，并在新终端窗口中运行，实时展示当前 Claude Code 会话的思考过程。

## 执行步骤

### 第一步：定位 claude-esp 二进制文件路径

优先使用环境变量：

```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

若变量为空，则从插件安装记录中查找：

```bash
cat ~/.claude/plugins/installed_plugins.json
```

找到 `claude-esp@alfie-qe` 对应的 `installPath`，拼接 `/bin/claude-esp.exe` 即为完整路径。

若上述均不可用，使用已知默认路径：

```
~/.claude/plugins/marketplaces/alfie-qe/plugins/claude-esp/bin/claude-esp.exe
```

将路径转换为 Windows 绝对路径（正斜杠转反斜杠），例如：

```
C:\Users\<用户名>\.claude\plugins\marketplaces\bank-qe\plugins\claude-esp\bin
```

### 第二步：验证文件存在

```bash
ls "${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe" 2>/dev/null || echo "NOT_FOUND"
```

若文件不存在，告知用户 claude-esp 插件未正确安装，并停止执行。

### 第三步：在新终端窗口中启动

将 `<BIN_DIR>` 替换为第一步获取的 bin 目录的 **Windows 绝对路径**（反斜杠）。

**优先尝试 Windows Terminal（更美观）：**

```bash
powershell.exe -Command "Start-Process wt -ArgumentList 'new-tab', '--title', '\"🧠 claude-esp\"', '--', 'cmd', '/k', 'cd /d <BIN_DIR> && .\\claude-esp.exe'"
```

**若上述失败，回退到普通 cmd 窗口：**

```bash
cmd.exe /c "start \"claude-esp\" cmd /k \"cd /d <BIN_DIR> && .\\claude-esp.exe\""
```

实际执行时只需运行其中一条，优先 Windows Terminal，失败后自动回退。

### 第四步：确认启动成功

告知用户：

> 已在新终端窗口中启动 claude-esp。
> claude-esp 会自动连接到当前 Claude Code 会话，实时展示思考过程。
> 若新窗口未弹出，请检查是否安装了 Windows Terminal，或直接在终端中手动运行：
> `cd <BIN_DIR> && .\claude-esp.exe`

## 注意事项

- 路径转换：bash 路径（`/c/Users/...`）需转换为 Windows 路径（`C:\Users\...`）再传给 `cmd.exe` 或 `powershell.exe`
- `.\claude-esp.exe` 无参数运行时进入**交互模式**，会自动选择最近的活跃会话
- 若需要指定会话，可提示用户先用 `/watch-session` 查询会话 ID，再手动在新窗口中追加 `-s <id>`
