#!/usr/bin/env node
/**
 * SessionStart hook: 首次启动自动配置 statusLine
 *
 * 逻辑：
 * 1. 读取 ~/.claude/settings.json
 * 2. 如果 statusLine 未配置 → 自动写入 Powerline 版配置
 * 3. 如果已配置 → 静默跳过
 *
 * @author Alfie
 */
'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const SETTINGS_PATH = path.join(os.homedir(), '.claude', 'settings.json');

// CLAUDE_PLUGIN_ROOT 由运行时注入，指向插件实际安装路径
const PLUGIN_ROOT = process.env.CLAUDE_PLUGIN_ROOT || '';

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_) {
    return null;
  }
}

function main() {
  if (!PLUGIN_ROOT) {
    // 无法获取插件路径，静默退出
    process.stdout.write(JSON.stringify({ suppressOutput: true }) + '\n');
    return;
  }

  // 统一使用正斜杠
  const scriptPath = PLUGIN_ROOT.replace(/\\/g, '/') + '/scripts/statusline-powerline.py';

  let settings = readJson(SETTINGS_PATH);

  if (settings && settings.statusLine) {
    // 已配置，跳过
    process.stdout.write(JSON.stringify({ suppressOutput: true }) + '\n');
    return;
  }

  // 未配置，自动写入
  if (!settings) {
    settings = {};
  }

  settings.statusLine = {
    type: 'command',
    command: `uv run ${scriptPath}`,
    padding: 2
  };

  try {
    fs.mkdirSync(path.dirname(SETTINGS_PATH), { recursive: true });
    fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings, null, 2), 'utf8');
  } catch (_) {
    // 写入失败，静默退出
  }

  process.stdout.write(JSON.stringify({ suppressOutput: true }) + '\n');
}

main();
