# Claude 插件安装指南

> **前置条件：** 已安装 Git、已生成 SSH Key（`~/.ssh/id_rsa`）、已在 GitLab 添加公钥

---

## 📌 30秒快速开始（复制粘贴即用）

### 1. 一键配置 SSH

#### Windows

```powershell
if (Test-Path "$env:USERPROFILE\.ssh\id_rsa") { $c="$env:USERPROFILE\.ssh\config"; $newConfig="`nHost gitlab.in.za`n    HostName gitlab.in.za`n    User git`n    Port 35001`n    IdentityFile ~/.ssh/id_rsa`n    PreferredAuthentications publickey"; if ((Test-Path $c) -and (Get-Content $c -ErrorAction SilentlyContinue | Select-String "Host\s+gitlab\.in\.za\b" -Quiet)) { $content = (Get-Content $c -Raw) -replace "(?ms)^Host\s+gitlab\.in\.za\b.*?(?=^Host\s|\z)", $newConfig.TrimStart(); $content | Set-Content $c -NoNewline; Write-Host "✅ 配置已更新" } else { $newConfig | Out-File -Append $c; Write-Host "✅ 配置已添加" }; git config --global url."git@gitlab.in.za:".insteadOf "http://gitlab.in.za/" } else { Write-Error "❌ SSH密钥不存在,请先生成 SSH Key" }
```

#### Mac/Linux

```bash
if [ -f ~/.ssh/id_rsa ]; then config_file=~/.ssh/config; new_config="\nHost gitlab.in.za\n    HostName gitlab.in.za\n    User git\n    Port 35001\n    IdentityFile ~/.ssh/id_rsa\n    PreferredAuthentications publickey"; if grep -q "Host gitlab\.in\.za" "$config_file" 2>/dev/null; then perl -i.bak -pe 'BEGIN{undef $/;} s/Host\s+gitlab\.in\.za\b.*?(?=\nHost\s|\z)/'"$(echo "$new_config" | sed 's/\\/\\\\/g; s/\//\\\//g; s/&/\\&/g')"'/s' "$config_file"; echo "✅ 配置已更新"; else echo -e "$new_config" >> "$config_file"; echo "✅ 配置已添加"; fi; git config --global url."git@gitlab.in.za:".insteadOf "http://gitlab.in.za/"; else echo "❌ SSH密钥不存在，请先生成 SSH Key"; exit 1; fi
```

### 2. 添加插件市场

```bash
claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git
```

### 3. 安装插件

```bash
claude plugin install za-qe@alfie-qe && claude plugin install za-qe-tools@alfie-qe
```

### 4. 验证安装

```bash
ssh -T git@gitlab.in.za && claude plugin marketplace list && claude plugin list
```

---

## 📖 详细说明

### 一、SSH配置说明

配置完成后，GitLab上任何项目的HTTPS地址都可以直接使用，会自动转换为SSH协议。

### 二、验证SSH连接

```bash
ssh -T git@gitlab.in.za
```

### 三、插件市场管理

```bash
claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git && claude plugin marketplace list
```

### 四、常用命令

```bash
claude plugin marketplace list  # 查看所有市场
claude plugin marketplace add <HTTPS地址>  # 添加市场
claude plugin marketplace remove <市场名>  # 移除市场
claude plugin install <插件名>@<市场名>  # 安装插件
claude plugin list  # 查看已安装插件
```

---

## ❓ 常见问题

**连接测试失败？**

```bash
ssh -Tv git@gitlab.in.za
```

**Permission denied？**

- 确认公钥已添加到GitLab
- 确认密钥文件正确：`~/.ssh/id_rsa`
- 确认端口是35001

**Host key verification failed？**
首次连接时输入`yes`接受主机密钥

**插件市场添加失败？**

```bash
claude plugin marketplace remove alfie-qe && claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git
```
