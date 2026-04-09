# za-dippy 插件 — Bash 命令智能审批系统

## 📌 概述

**za-dippy** 是 Claude Code 的**Bash 命令智能审批系统**，自动放行安全命令，拦截危险操作。告别权限确认疲劳，让 Claude 在安全前提下流畅执行代码操作。

> **核心特性：自动化、精准、可定制的命令安全防护。**

---

## ✨ 核心功能

- 🚀 **自动放行** — 内置 500+ 安全命令的智能识别库，自动批准只读操作
- 🛑 **拦截危险** — 拦截 `rm -rf`、`git push --force` 等破坏性操作，拒绝权限滥用
- ⚡ **零额外步骤** — 省去繁琐的权限弹框，保持编码流畅性
- 🎯 **精准分类** — 基于命令语义识别，支持 100+ 常用工具（git、docker、kubectl、npm 等）
- 📝 **可定制规则** — 项目级 `.dippy` 配置，快速适配团队工作流

---

## 🔍 工作原理

### 决策流程

```
Bash 命令执行
    ↓
dippy-hook 拦截
    ↓
内置白名单检查 ← SIMPLE_SAFE (500+ 只读命令)
    ↓
专用工具分析器 ← git、docker、curl、npm 等
    ↓
配置规则匹配 ← ~/.dippy/config 或 project/.dippy
    ↓
    ├─ 安全命令 → ✅ 自动批准
    ├─ 可疑命令 → ❓ 询问用户
    └─ 危险命令 → ❌ 自动拦截
```

### 支持的工具分析器

| 工具类别 | 支持工具 | 特性 |
|---------|---------|------|
| **VCS** | git | 检测 push --force、reset --hard 等 |
| **容器** | docker、podman | 检测 rm、exec、run 等 |
| **集群** | kubectl、helm | 检测 delete、apply 等 |
| **包管理** | npm、pip、cargo | 检测 uninstall、publish 等 |
| **网络** | curl、wget | 检测 POST、PUT、DELETE 等 |
| **系统** | rm、chmod、sudo | 检测文件删除、权限变更 |
| **云** | aws、gcloud、az | 检测 delete、modify 等 |

---

## 📦 安装与配置

### 第一步：安装插件

在 Claude Code 中启用 `za-dippy@alfie-qe` 插件。

### 第二步：运行安装 Skill

```bash
/za-dippy:install
```

此 Skill 会自动：
1. 将 dippy-hook 写入 `~/.claude/settings.json`
2. 启用 `dippy@alfie-qe` 插件
3. 部署默认配置到 `~/.dippy/config`
4. 重启 Claude Code 后生效

### 第三步：验证安装

```bash
# 查看 hook 是否已注册
cat ~/.claude/settings.json | grep dippy-hook

# 查看默认配置
cat ~/.dippy/config
```

---

## ⚙️ 配置规则

### 默认配置位置

```
~/.dippy/config              # 用户级配置（全局）
<项目根>/.dippy              # 项目级配置（优先级更高）
```

### 规则语法

#### 允许规则
```bash
# 前缀匹配 — 允许 "cmd" 和 "cmd <任意参数>"
allow mvn --version

# 精确匹配 — 仅允许 "cmd" 不带参数（|后缀表示精确）
allow make help|
```

#### 拒绝规则
```bash
# 拒绝并显示消息
deny rm -rf "这是非常危险的操作！"
```

### 配置示例

#### 全局配置（`~/.dippy/config`）
```bash
# -- Maven 安全操作 --
allow mvn --version
allow mvn validate
allow mvn help:describe
allow mvn dependency:tree

# -- Git 危险操作 --
deny git push --force "Force push 已被禁止，请使用 -u 重新提交"
allow git log
allow git status

# -- 系统命令 --
deny rm -rf "危险：递归删除已被禁止"
allow ls
allow cat
```

#### 项目级配置（`<项目>/.dippy`）
```bash
# Bash 命令安全配置
allow bash --version
allow bash -c
allow bash -n

# 项目特定的危险命令拦截
deny npm publish "请先在 CI/CD 中验证"
```

---

## 🛠️ Skills 说明

| Skill 名称 | 触发场景 | 功能 |
|-----------|---------|------|
| `install` | 用户执行 `/za-dippy:install` | 自动配置 hook、启用插件、部署配置 |

---

## 📊 常见场景

### 场景 1：开发者快速迭代（省去权限弹框）

**不使用 dippy：**
```
Claude 执行: rm old_file.txt
↓
Claude Code 弹框: "需要确认？" 
↓ (用户点击 approve)
执行成功
```

**使用 dippy：**
```
Claude 执行: rm old_file.txt
↓
dippy 自动检查 → "只读操作"
↓
✅ 自动批准，无需用户干预
```

### 场景 2：防止破坏性操作

```bash
Claude 尝试: git push --force
↓
dippy 检测 → "危险操作"
↓
❌ 自动拒绝，并提示用户
```

### 场景 3：团队工作流定制

在项目根目录创建 `.dippy`：
```bash
# 允许测试命令
allow npm run test
allow npm run lint

# 禁止生产部署
deny npm publish "CI/CD 管道中发布，禁止本地发布"
deny docker push "请通过 GitLab CI 发布镜像"
```

---

## 🔒 安全策略

### 默认白名单（SIMPLE_SAFE）

内置 500+ 只读命令自动批准：
- 文件查看：`cat`、`less`、`head`、`tail`
- 搜索工具：`grep`、`find`（仅查询）、`locate`
- 版本查询：`--version`、`--help`、`-v`
- Git 查询：`git log`、`git status`、`git diff`
- 系统查询：`ls`、`pwd`、`whoami`、`uname`

### 专用工具分析器

**Git 智能检测：**
- ✅ 允许：`git log`、`git diff`、`git show`、`git clone`
- ❌ 拦截：`git push --force`、`git reset --hard`、`git rebase -i`

**Docker 智能检测：**
- ✅ 允许：`docker ps`、`docker images`、`docker logs`
- ❌ 拦截：`docker rm -f`、`docker exec -it bash`

**NPM 智能检测：**
- ✅ 允许：`npm list`、`npm show`、`npm audit`
- ❌ 拦截：`npm uninstall`、`npm publish`

---

## 📝 日志查看

### 查看审批决策日志

```bash
# 用户级日志
cat ~/.claude/hook-approvals.log

# 查看最近 10 条决策
tail -n 10 ~/.claude/hook-approvals.log

# 搜索特定命令
grep "git push" ~/.claude/hook-approvals.log
```

日志格式：
```
2026-04-09 18:57:15 [INFO] [ALLOW] git log --oneline
2026-04-09 18:57:20 [WARNING] [ASK] docker push registry.com/app:latest
2026-04-09 18:57:25 [DENY] git push --force (user config rule)
```

---

## 🚀 高级用法

### 查询现有规则

```bash
# 显示所有加载的规则（优先级排序）
cat ~/.dippy/config
```

### 动态启用/禁用

通过环境变量临时禁用 dippy：

```bash
DIPPY_DISABLE=1 bash -c "rm -rf /"  # 临时绕过（仅演示，实际不推荐）
```

### 跨工具集成

**与其他安全工具集成：**
- 结合 git hooks 防止误操作
- 与 CI/CD 管道联动
- 配合日志审计系统

---

## ⚠️ 故障排除

### Hook 无法生效

**问题：** 执行 Bash 命令时没有权限提示

**解决：**
```bash
# 1. 检查 hook 是否已注册
grep "dippy-hook" ~/.claude/settings.json

# 2. 检查插件是否启用
grep "dippy@alfie-qe" ~/.claude/settings.json

# 3. 重启 Claude Code
# (关闭后重新打开)
```

### 规则不生效

**问题：** 预期被拦截的命令仍然执行了

**检查清单：**
1. 项目级 `.dippy` 是否存在？（优先级最高）
2. 用户级 `~/.dippy/config` 是否存在？
3. 规则语法是否正确？运行 `cat ~/.dippy/config` 验证
4. 查看日志了解实际匹配情况

### 误拦截安全命令

**问题：** 某个安全命令被错误拦截

**解决：**
在项目 `.dippy` 中添加 allow 规则：
```bash
allow my_safe_command
```

---

## 📚 参考资源

| 资源 | 路径 |
|-----|------|
| **默认配置** | `~/.dippy/config` |
| **项目配置** | `<项目根>/.dippy` |
| **日志文件** | `~/.claude/hook-approvals.log` |
| **源代码** | [Za-Dippy](http://gitlab.in.za/claude/alfie/qe/-/tree/main/plugins/za-dippy) |

---

## 🔗 相关命令

- `/za-dippy:install` — 安装并配置 dippy
- `/esp` — 启动 esp 事件流查看工具

---

## 💬 反馈与贡献

遇到 bug 或有建议？请提交 issue 到项目仓库：
```
https://gitlab.in.za/claude/alfie/qe/-/issues
```

---

## 📋 版本信息

| 项目 | 值 |
|-----|-----|
| **版本** | v0.2.7 |
| **作者** | Lily Dayton |
| **平台** | Windows、macOS、Linux |
| **依赖** | Python 3.8+ |

---

**让 Claude Code 自由奔跑，同时筑起安全防线！** 🛡️✨

