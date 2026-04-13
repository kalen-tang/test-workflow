#!/usr/bin/env node
/**
 * SessionStart hook: za-qe-tools 自动初始化
 *
 * 逻辑：
 * 1. 确保 ~/.claude/za-qe-tools.json 配置文件存在
 * 2. 根据 statusline 配置自动写入 settings.json
 * 3. 如果 dippy 已启用，确保 ~/.dippy/config 存在
 *
 * @author Alfie
 */
'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const SETTINGS_PATH = path.join(os.homedir(), '.claude', 'settings.json');
const CONFIG_PATH   = path.join(os.homedir(), '.claude', 'za-qe-tools.json');
const DIPPY_CONFIG  = path.join(os.homedir(), '.dippy', 'config');

const PLUGIN_ROOT = process.env.CLAUDE_PLUGIN_ROOT || '';

const DEFAULT_CONFIG = {
  statusline: { enabled: true, mode: 'powerline' },
  notify:     { enabled: false },
  dippy:      { enabled: false },
  esp:        { enabled: false }
};

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_) {
    return null;
  }
}

function ensureModuleConfig() {
  if (fs.existsSync(CONFIG_PATH)) return readJson(CONFIG_PATH);

  // 首次启动，创建默认配置
  try {
    fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(DEFAULT_CONFIG, null, 2), 'utf8');
  } catch (_) {}

  return DEFAULT_CONFIG;
}

function setupStatusline(config, settings) {
  if (!PLUGIN_ROOT) return settings;

  const slConfig = config.statusline || {};
  if (!slConfig.enabled) {
    // statusline 关闭时不主动删除已有配置（用户可能手动配置了）
    return settings;
  }

  if (settings.statusLine) {
    // 已配置，跳过
    return settings;
  }

  // 未配置，根据 mode 自动写入
  const scriptName = slConfig.mode === 'standard' ? 'statusline.py' : 'statusline-powerline.py';
  const scriptPath = PLUGIN_ROOT.replace(/\\/g, '/') + '/scripts/' + scriptName;

  settings.statusLine = {
    type: 'command',
    command: `uv run ${scriptPath}`,
    padding: 2
  };

  return settings;
}

function setupDippy(config) {
  if (!config.dippy || !config.dippy.enabled) return;
  if (!PLUGIN_ROOT) return;

  // 确保 ~/.dippy/config 存在
  if (fs.existsSync(DIPPY_CONFIG)) return;

  const defaultDippy = path.join(PLUGIN_ROOT, 'config', 'default.dippy');
  if (!fs.existsSync(defaultDippy)) return;

  try {
    fs.mkdirSync(path.dirname(DIPPY_CONFIG), { recursive: true });
    fs.copyFileSync(defaultDippy, DIPPY_CONFIG);
  } catch (_) {}
}

function main() {
  const config = ensureModuleConfig();

  let settings = readJson(SETTINGS_PATH);
  if (!settings) settings = {};

  const originalSettings = JSON.stringify(settings);
  settings = setupStatusline(config, settings);

  // 仅在配置有变化时写入
  if (JSON.stringify(settings) !== originalSettings) {
    try {
      fs.mkdirSync(path.dirname(SETTINGS_PATH), { recursive: true });
      fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings, null, 2), 'utf8');
    } catch (_) {}
  }

  setupDippy(config);

  process.stdout.write(JSON.stringify({ suppressOutput: true }) + '\n');
}

main();
