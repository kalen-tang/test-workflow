# Claude 插件安装

> **前置条件：** 已安装 Git、已生成 SSH Key（`~/.ssh/id_rsa`）、已在 GitLab 添加公钥

---

## 📌 30秒快速开始（复制粘贴即用）

### 一键配置

#### windows

```powershell
if (Test-Path "$env:USERPROFILE\.ssh\id_rsa") { $c="$env:USERPROFILE\.ssh\config"; $newConfig="`nHost gitlab.in.za`n    HostName gitlab.in.za`n    User git`n    Port 35001`n    IdentityFile ~/.ssh/id_rsa`n    PreferredAuthentications publickey"; if ((Test-Path $c) -and (Get-Content $c -ErrorAction SilentlyContinue | Select-String "Host\s+gitlab\.in\.za\b" -Quiet)) { $content = (Get-Content $c -Raw) -replace "(?ms)^Host\s+gitlab\.in\.za\b.*?(?=^Host\s|\z)", $newConfig.TrimStart(); $content | Set-Content $c -NoNewline; Write-Host "✅ 配置已更新" } else { $newConfig | Out-File -Append $c; Write-Host "✅ 配置已添加" }; git config --global url."git@gitlab.in.za:".insteadOf "http://gitlab.in.za/" } else { Write-Error "❌ SSH密钥不存在,请先生成 SSH Key" }
```

#### mac/linux

```bash
if [ -f ~/.ssh/id_rsa ]; then config_file=~/.ssh/config; new_config="\nHost gitlab.in.za\n    HostName gitlab.in.za\n    User git\n    Port 35001\n    IdentityFile ~/.ssh/id_rsa\n    PreferredAuthentications publickey"; if grep -q "Host gitlab\.in\.za" "$config_file" 2>/dev/null; then perl -i.bak -pe 'BEGIN{undef $/;} s/Host\s+gitlab\.in\.za\b.*?(?=\nHost\s|\z)/'"$(echo "$new_config" | sed 's/\\/\\\\/g; s/\//\\\//g; s/&/\\&/g')"'/s' "$config_file"; echo "✅ 配置已更新"; else echo -e "$new_config" >> "$config_file"; echo "✅ 配置已添加"; fi; git config --global url."git@gitlab.in.za:".insteadOf "http://gitlab.in.za/"; else echo "❌ SSH密钥不存在，请先生成 SSH Key"; exit 1; fi
```

# 2. 添加插件市场

```bash
claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git
```

# 3. 安装插件

```bash
claude plugin install za-qe@alfie-qe
claude plugin install za-qe-tools@alfie-qe
```

**验证：**

```bash
ssh -T git@gitlab.in.za  # 测试连接
claude plugin marketplace list  # 查看已添加的市场
claude plugin list  # 查看已安装的插件
```

---

## 📖 详细说明

### 一、一键配置 SSH Config

配置完成后，GitLab 上任何项目的 HTTPS 地址都可以直接使用，会自动转换为 SSH 协议。

---

### 二、验证 SSH 连接

```bash
ssh -T git@gitlab.in.za
# 成功输出：Welcome to GitLab, @你的用户名!
```

---

### 三、添加插件市场

```bash
claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git
claude plugin marketplace list  # 确认添加成功
```

---

### 四、安装插件

```bash
claude plugin install za-qe@alfie-qe
claude plugin list  # 查看已安装的插件
```

---

### 五、常用命令

```bash
# 插件市场管理
claude plugin marketplace list                 # 查看所有市场
claude plugin marketplace add <HTTPS地址>      # 添加市场
claude plugin marketplace remove <市场名>      # 移除市场

# 插件管理
claude plugin install <插件名>@<市场名>        # 安装插件
claude plugin list                             # 查看已安装插件
```

---

### 六、常见问题

**连接测试失败？**

```bash
ssh -Tv git@gitlab.in.za  # 查看详细错误
```

**Permission denied？**

- 确认公钥已添加到 GitLab
- 确认密钥文件正确：`~/.ssh/id_rsa`
- 确认端口是 35001

**Host key verification failed？**
首次连接时输入 `yes` 接受主机密钥

**配置文件格式？**

```
Host gitlab.in.za
    HostName gitlab.in.za
    User git
    Port 35001
    IdentityFile ~/.ssh/id_rsa
    PreferredAuthentications publickey
```

**插件市场添加失败？**

```bash
claude plugin marketplace remove alfie-qe        # 先移除
claude plugin marketplace add http://gitlab.in.za/claude/alfie/qe.git  # 重新添加
```

---

**📌 核心提示：** 配置完成后，GitLab 上任何项目的 HTTPS 地址都可以直接 `git clone`，会自动转换为 SSH 协议。

## 系统架构

![测试案例生成与自动化流程](https://plantuml.in.za/svg/jLXRJnj757xVNp5DLGKSsGItgLAaLWAZA9KQDPTMVIXLjR47UsMpwwpN8QIAP21WRC0c8aL9YRY4SaaKcQP96Z26_9VMixj-ob_eNFOoksi75LG_iJDdpcs-yvqpVAIbu0W4sOmeoK8kBSbPKHL7m4qndawgIbvEn9ICeeBHbAH1RZ-BzyKalA6DPI1GOLmJvMI65uWh8rb5XhBMMIG1XyLyHhkaO27fBWIzvxbDMKd07Co2p_b5LPJJrgAWIHhMgx-PDNT_rTTdcaUpniDLVMQXkLSnYyzHUGVDBUblnesTMK6ml0LdK6KLRSyswzkeM3TApyw0NmI0VuwpjaJhIK5_EQ4l5VNrZJD0p67BezVXhK4btbxUh1sPjNMl_23CIKcvtP560LKVD0ysZBLnAfnJup4SRdlLg3ADgd-o26tLbwMSfgXZ_WEjZPNc_fQnkcdkJgFw8fKUXb8kbVz1Ial2FIuHtobA9cU7xwpUI4iPTzcdNOMtmlWQSb0TaldycDiR-ih2a8ogkwr2gGyzNK7bDVo1hqOlREiR1NrrapbE4qXjW8y7BiI-6BZOpaw2viqnnQUMcQBA4dPsZzKN5tCmpCI9FhqqYzvkyhXX5gZM4L7EYvaOFc6fxRz85BTrKuc7LNXRWgDkGb1jnQZyuGqvbeBnjAMDkDZV8UZRk0Jbi2YBcR6xH2D3YRwqZvr4CzDkt5JmM8LYLWed8OvOn4Z1KLSsKNM3AmmIFYiOgXQB1oF6WF70uqhiQWTinAvy0_0kjbDTQ1ujuq-MskQxTNryruSDA-klTrh5ghbx7mT7NOYFPAx4inzA-IMAPK30p5lpmHvDJw7QljycnOzHcj6Vl33V7PfxpxdgECOigKqmA0qFyqPP-QAtDTIOODVZhu33bsXntfoRHCkl-Vl3UgYzpbVtFOPMb1hbxB4Bv4WZJwJYMEeOxw-gofqnZwRo8fgROZT3DMM9XD-dUnwwCBVlaqZcbZZgn2TbHHqHCvYx4z_cjMnUomNvDCYaRMaqGA29ZkpfvyDKUp9qyL2TC0kJGt8N0psx2sQfcof8oyfe1YQIS03NlL-DTS_LHthW6g_3hA9g94-1U7aYqCkRw47PGmVif9DlDy_1TjQcHLaCHeLmMCR1ehvodnJrMWCrgjq-8ii5KksGW9j3CQyfJDWRZLxQDjVdg8KdNFJm3enVXpdSl0NXx9Sd-GbdWV7YHNElq7hqbrvxyxxncwyrW_1NW3QfBjQKUZ22kybY48edTG7xq1i1tbPcwHQSVW_22MLKndQvxYNmdSox3_f0_zVdclKwlY7q-xo-jjUbbmyn4ABdF-ac5gCHuEred4LdOd2KUhkSu6jw0QbZhNyQ0Npzw4zV6GlJWZjHE2eP6GiM9zkhLgbXC-maMgZmweY5poB0LtcOTL1rIN074KUTmxw2oyFsdgSeYS50yJ8pnEQ520ZIiM1DLMwM6FCADWFpwrP1zW7CtRWhCJtdU0e_9T3hSmxGWm0ciEx46oS6Tv2REQJoBDG7pAD5DBKfU8ULi2ebKrexSUQUENc8oikdhV_IXz9oZZ40IG_FUVz3IZYw922OscbDxbXPyO-4JbwyP_J7TPmHnjcdImfQNdQImeTDoS_BtImpXA9Fd1C-2ZiRRZTm_dB3ThcVHCsCdx8s7ZhnElVj2_HzOyOycaBbPop1xnkb4mVicPkSgDn0-u3rZgIC8ZZ3KLjHDfMr2WVcqGF1cQ7RYz9KsLM3iQX1S5FHD6K4ACE-VXqAyHVF_0c51Bh3ODc7Fu6dT_rJ6ESR2_xagHb_1YSPff2fnmyDF3mmjHxKiP1uUBi31oj7A2S02ISGb9SvgB5EDFVVe-iK3j5Gh3CDVnUU0glFSgyDqDNVCz0JwndijaHufz3kVkjm0TMtc7Us4jfzMiLvOs8V7TJDMiq-kb5fFNw6L_MrelvgnvyB2WII2cvYOjVhdwlwM0Q8JdDhsbXUCYf5us0LHsoj6erww_5RL9rlRStONh4tLkCHlWlBAzU-CrFsPp9jXiXGw5flSw-CvikujgxrHdfnJOL2-0spMZVM2qxvCRmEoTISzmt9a65j1H33rfrt8Vdml6le77chz-TUpzibuE0iTh3dMfJtD8g_7NVvAQgvL-4BXXaDZdUyVy5HZEtQtaKz_rZmUXTbtX6def6evG_36SCEzeVTBNaGDkgyFtm1UFBbVMgI9UVzndoA4f_iTmDnYkOm_6DAIYIW_1DZ7kgwlHiDxc8bmhr_0G00)
