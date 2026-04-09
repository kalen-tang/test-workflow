# alfie 插件规范（本项目适用摘要）

本文档摘自 alfie 分发体系 `base/README-plugin.md`，仅保留与 qe 仓库相关的规范要点。

---

## 当前项目状态

- **仓库类型**：插件仓库（存在 `.claude-plugin/marketplace.json`）
- **Marketplace**：`alfie-qe`
- **插件数量**：2 个（`za-qe` core + `za-qe-tools` optional）
- **安装方式**：`claude plugin marketplace add` + `claude plugin install`

---

## 命名规范

### 插件命名

格式：`za-{域}-{功能}`

| 模式 | 示例 | 说明 |
|------|------|------|
| `za-{域}` | `za-qe` | 该域的核心插件（无功能后缀） |
| `za-{域}-{功能}` | `za-qe-spec` | 该域的专项扩展插件 |
| `za-{域}-exp` | `za-qe-exp` | 该域的实验性插件 |

域前缀 `qe` 对应质量工程（测试/QE）方向。

### Skill 命名

```
<岗位前缀>-功能域-类型后缀
```

- 若 skill 名已含明确的框架/领域前缀（如 `devplan-`），可省略岗位前缀
- 通用名必须加岗位前缀 `qe-`，避免跨仓库冲突

**标准类型后缀**：

| 后缀 | 类型 | 示例 |
|------|------|------|
| `-spec` | 开发规范 | `qe-test-spec` |
| `-guide` | 使用指南 | `qe-api-guide` |
| `-tool` | 工具功能 | `case-designer` |

### Skill description 字段格式

```
[核心功能说明]。用于[使用场景]。当需要[触发条件]时使用。涉及[关键词列表]等关键词时使用此skill。
```

### Command 命名

格式：`domain-action`，全小写，连字符分隔。如 `qe-quick`、`manual-case`。

---

## 目录结构规范

### marketplace.json

```json
{
  "name": "alfie-qe",
  "owner": { "name": "Alfie" },
  "plugins": [
    { "name": "za-qe", "source": "./plugins/za-qe", "description": "...", "category": "core" }
  ]
}
```

- 不含 `version`/`author`/`strict`（这些在 plugin.json 中声明）
- `category`：`core`（强制安装）/ `optional`（用户可选）

### plugin.json

- **必须放在** `.claude-plugin/` 子目录下
- 声明 `commands`/`skills` 路径，否则官方 CLI 无法正确加载
- `${CLAUDE_PLUGIN_ROOT}`：官方运行时变量，自动替换为插件实际安装路径

```json
{
  "name": "za-qe",
  "version": "1.3.0",
  "description": "...",
  "author": { "name": "Alfie" },
  "commands": ["./commands/"],
  "skills": ["./skills/"]
}
```

### session-start-content.md

放在 `hooks/` 目录下。alfie-install 安装时自动合并到 `~/.claude/hooks/session-start-content.md`，由 za-base 的 `session-banner.js` 统一输出。各插件不需要单独注册 SessionStart hook 来输出此内容。

---

## 当前不需要的文件

| 文件 | 原因 |
|------|------|
| `skills.json`（预构建索引） | 纯工具类插件不需要，Claude 原生从插件缓存加载 |
| `category.json` | 标准仓库用，插件仓库不需要 |
| `prompt-hook.config.json` | 可选文件，当前无需拦截注入 |
| SessionStart/UserPromptSubmit hooks 脚本 | skills.json 合并由 za-base 统一处理 |
| `installer/uninstall_legacy.js` | 未使用过旧版安装方式 |

---

## 扩展时参考（渐进式披露）

以下内容在当前单插件结构下暂不需要，扩展时查阅完整规范 `base/README-plugin.md`。

### 拆分为多插件

**时机**：Skills 数量明显增多（>15 个）且需区分 core/optional 时。

**模式**（参照 backend）：

```
plugins/
├── za-qe/          # 核心：命令 + hooks（category: core）
├── za-qe-tools/    # 工具类 skill（category: core）
├── za-qe-spec/     # 规范类 skill（category: optional）
└── za-qe-exp/      # 实验性命令 + MCP（category: optional）
```

**注意**：
- hooks 只在核心命令插件中声明
- 多插件的 SessionStart hook 脚本名必须不同，否则 Claude 去重后只执行一个
- 拆分后 `skills.json` 仅规范类插件（需 `skill-index` 索引）需要，工具类不需要
- 每个含 skill 的拆分插件需要 `category.json`：`{ "label": "显示名", "optional": true/false }`

### 添加 hooks

在 plugin.json 中声明：

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "node ${CLAUDE_PLUGIN_ROOT}/hooks/xxx.js", "timeout": 10 }] }],
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/xxx.py", "timeout": 30 }] }]
  }
}
```

**注意**：不要同时使用外部文件引用（`"hooks": "./hooks/hooks.json"`）和 `hooks/hooks.json` 文件，官方 CLI 会自动扫描 `hooks/` 目录导致重复加载报错。推荐直接内联到 plugin.json。

### 添加 MCP 服务器

在 plugin.json 中声明，通过 wrapper 脚本处理 pip 依赖：

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/start.py"]
    }
  }
}
```

### prompt-hook.config.json

声明哪些命令/skill 触发时需注入 skills 索引提示，alfie-install 安装后自动合并到全局：

```json
{
  "intercept": {
    "commands": ["requirement-clarify", "code"],
    "skills": ["msf-service-spec"]
  }
}
```

### skills.json（预构建索引）

规范类插件（需被 `skill-index` 命令检索的）提供预构建索引：

```json
[
  {
    "name": "skill-name",
    "description": "...",
    "when_to_use": "...",
    "keywords": ["..."],
    "category": "qe",
    "level": "user_level"
  }
]
```

### 旧版卸载脚本

如果项目之前使用过 `setup_wf_tools.py` 安装方式，需在 `installer/` 下创建 `uninstall_legacy.js` + `uninstall_tip.txt`，清理 `~/.claude/` 下的旧版残留。
