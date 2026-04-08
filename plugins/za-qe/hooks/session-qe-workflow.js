#!/usr/bin/env node
// @author Alfie
// Session Start Hook for za-qe:
//   1. Merge skills.json from all installed plugins → ~/.claude/skills/skills.json
//   2. Output session-start-content.md as systemMessage
// Node.js built-ins only, no npm required.

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const CLAUDE_DIR        = path.join(os.homedir(), '.claude');
const INSTALLED_PLUGINS = path.join(CLAUDE_DIR, 'plugins', 'installed_plugins.json');
const USER_SKILLS_DIR   = path.join(CLAUDE_DIR, 'skills');
const USER_SKILLS_JSON  = path.join(USER_SKILLS_DIR, 'skills.json');

// ─── Skills merge ────────────────────────────────────────────────────────────

/**
 * Read and parse a JSON file. Returns null on any error.
 */
function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_) {
    return null;
  }
}

/**
 * Extract skills array from a skills.json (supports array or {skills:[]} formats).
 */
function extractSkills(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.skills)) return data.skills;
  return [];
}

/**
 * Compute a simple content hash to detect changes across sessions.
 * Uses total entry count + sorted name list.
 */
function contentHash(entries) {
  return entries.length + ':' + entries.map(e => e.name || '').sort().join(',');
}

/**
 * Scan all installed plugins for skills.json files and merge them into
 * ~/.claude/skills/skills.json. Uses a hash-based flag to skip when unchanged.
 */
function mergePluginSkills() {
  const installed = readJson(INSTALLED_PLUGINS);
  if (!installed) return;

  const allEntries = [];
  const pluginVersions = [];

  for (const [key, instances] of Object.entries(installed)) {
    if (!Array.isArray(instances)) continue;
    for (const inst of instances) {
      const installPath = inst.installPath;
      if (!installPath) continue;

      // skills.json may be at root or in skills/ subdir
      const candidates = [
        path.join(installPath, 'skills.json'),
        path.join(installPath, 'skills', 'skills.json'),
      ];
      for (const candidate of candidates) {
        const data = readJson(candidate);
        const entries = extractSkills(data);
        if (entries.length > 0) {
          allEntries.push(...entries);
          pluginVersions.push(`${key}@${inst.version || 'unknown'}`);
          break;
        }
      }
    }
  }

  if (allEntries.length === 0) return;

  // Deduplicate by name (last wins)
  const deduped = {};
  for (const entry of allEntries) {
    if (entry.name) deduped[entry.name] = entry;
  }
  const merged = Object.values(deduped);

  // Check if update needed via hash flag
  const flagFile = path.join(USER_SKILLS_DIR, '.plugin-skills-hash');
  const newHash  = contentHash(merged) + '|' + pluginVersions.sort().join(',');
  const oldHash  = fs.existsSync(flagFile)
    ? fs.readFileSync(flagFile, 'utf8').trim()
    : '';

  if (newHash === oldHash) return;

  // Read existing user skills.json (may contain project-level entries)
  const existing = extractSkills(readJson(USER_SKILLS_JSON));

  // Remove stale plugin entries (those previously written by this hook)
  const nonPlugin = existing.filter(e => e.source !== 'plugin');

  // Tag new entries as plugin-sourced
  const tagged = merged.map(e => ({ ...e, source: 'plugin' }));

  // Final merge: non-plugin entries first, then plugin entries
  const finalMap = {};
  for (const e of [...nonPlugin, ...tagged]) {
    if (e.name) finalMap[e.name] = e;
  }
  const final = Object.values(finalMap);

  // Write
  fs.mkdirSync(USER_SKILLS_DIR, { recursive: true });
  fs.writeFileSync(
    USER_SKILLS_JSON,
    JSON.stringify({ _comment: 'Auto-generated. Plugin skills tagged with source:plugin.', skills: final }, null, 2),
    'utf8'
  );
  fs.writeFileSync(flagFile, newHash, 'utf8');
}

// ─── Main ────────────────────────────────────────────────────────────────────

function main() {
  // Merge plugin skills silently (errors must not break the hook)
  try {
    mergePluginSkills();
  } catch (_) {}

  // Session content is handled by za-base session-banner.js,
  // which reads ~/.claude/hooks/session-start-content.md (merged by installer).
  process.stdout.write(JSON.stringify({ suppressOutput: true }) + '\n');
}

main();
