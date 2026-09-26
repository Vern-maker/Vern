#!/usr/bin/env python3
"""Offline checks for this workspace's documented JSON/YAML subset; not a full schema validator."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILLS = {
    'vern-sop', 'vern-market-insight', 'vern-project-coordination',
    'vern-website-seo', 'vern-meeting-minutes', 'vern-excel-dashboard',
    'vern-product-development',
}
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SEMVER = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$')


def validate(root: Path) -> list[str]:
    root = root.resolve()
    plugin = root / 'plugins' / 'vern-workspace'
    errors: list[str] = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def read_json(path):
        try:
            value = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(value, dict):
                raise ValueError('expected JSON object')
            return value
        except (OSError, ValueError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
            return {}

    portable = read_json(plugin / 'plugin.json')
    legacy = read_json(plugin / '.codex-plugin/plugin.json')
    marketplace = read_json(root / '.agents/plugins/marketplace.json')
    check(portable.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'portable schema must be declared')
    for key in ('name', 'version', 'description', 'author', 'repository', 'keywords'):
        check(bool(portable.get(key)) and portable.get(key) == legacy.get(key), f'manifest identity mismatch or missing: {key}')
    check(portable.get('name') == plugin.name, 'plugin name must match folder')
    check(bool(SEMVER.fullmatch(str(portable.get('version', '')))), 'version must use the workspace release format major.minor.patch')
    check(legacy.get('skills') == './skills/', 'legacy skills path must be ./skills/')
    check('extensions' not in portable, 'this layout uses the compatibility overlay, not an inline extension')
    check(not any(k in legacy for k in ('apps', 'mcpServers', 'hooks')), 'planned integrations must not be declared as active components')
    interface = legacy.get('interface', {})
    if not isinstance(interface, dict):
        errors.append('interface must be an object')
        interface = {}
    for key in ('displayName', 'shortDescription', 'longDescription', 'developerName', 'category'):
        check(isinstance(interface.get(key), str) and bool(interface.get(key)), f'missing interface.{key}')
    prompts = interface.get('defaultPrompt', [])
    check(isinstance(prompts, list) and 1 <= len(prompts) <= 3 and all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts), 'defaultPrompt must contain 1-3 strings of 1-128 characters')
    entries = marketplace.get('plugins', [])
    check(isinstance(marketplace.get('name'), str) and bool(re.fullmatch(r'[A-Za-z0-9_-]+', marketplace.get('name', ''))), 'invalid marketplace name')
    check(isinstance(entries, list) and len(entries) == 1, 'this workspace must declare exactly one plugin')
    if isinstance(entries, list) and len(entries) == 1 and isinstance(entries[0], dict):
        entry = entries[0]
        check(entry.get('name') == plugin.name, 'marketplace plugin name mismatch')
        check(entry.get('source') == {'source': 'local', 'path': './plugins/vern-workspace'}, 'marketplace path must resolve from repository root')
        check(entry.get('policy') == {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'unexpected marketplace policy')
        check(entry.get('category') == 'Productivity', 'marketplace category missing')

    found = {p.name for p in (plugin / 'skills').glob('*') if p.is_dir()}
    check(found == SKILLS, f'skill set mismatch: missing {sorted(SKILLS-found)}, extra {sorted(found-SKILLS)}')
    for name in sorted(found):
        base = plugin / 'skills' / name
        try:
            text = (base / 'SKILL.md').read_text(encoding='utf-8')
            match = re.match(r'^---\nname: ([^\n]+)\ndescription: ("[^\n]*")\n---\n', text)
            if not match:
                raise ValueError('frontmatter must use this workspace\'s name + JSON-quoted description subset')
            check(match[1] == name and bool(NAME.fullmatch(name)) and len(name) <= 64, f'{name}: invalid name')
            description = json.loads(match[2])
            check(bool(description) and len(description) <= 1024, f'{name}: invalid description')
            check(len(text[match.end():].strip()) > 100, f'{name}: empty instructions')
            check('[TODO:' not in text, f'{name}: unfinished scaffold')
            check((base / 'references/deliverable.md').is_file(), f'{name}: missing deliverable reference')
            ui = (base / 'agents/openai.yaml').read_text(encoding='utf-8')
            values = {}
            for key in ('display_name', 'short_description', 'default_prompt'):
                m = re.search(r'^  ' + key + r': ("[^\n]*")$', ui, re.M)
                if not m:
                    raise ValueError(f'missing quoted interface.{key}')
                values[key] = json.loads(m[1])
            check(25 <= len(values['short_description']) <= 64, f'{name}: UI short description length must be 25-64')
            check('$' + name in values['default_prompt'], f'{name}: default prompt must mention skill')
            check('  allow_implicit_invocation: true' in ui, f'{name}: implicit invocation must be enabled')
        except (OSError, ValueError) as exc:
            errors.append(f'{name}: {exc}')

    # All packaged skill/reference links must remain in the plugin. Repository docs may link inside the repo.
    for doc in root.rglob('*.md'):
        if any(part in ('cases', '.git', '__pycache__') for part in doc.relative_to(root).parts):
            continue
        try:
            body = doc.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{doc.relative_to(root)}: {exc}')
            continue
        body = re.sub(r'```.*?```', '', body, flags=re.S)
        boundary = plugin if doc.is_relative_to(plugin / 'skills') or doc.is_relative_to(plugin / 'references') else root
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            resolved = (doc.parent / unquote(parsed.path)).resolve()
            check(resolved.is_relative_to(boundary) and resolved.exists(), f'{doc.relative_to(root)}: missing or escaping link {target}')

    registry = read_json(plugin / 'references/integrations/registry.json')
    integrations = registry.get('integrations', [])
    check(registry.get('configuration_kind') == 'planning-only', 'registry must be planning-only')
    if isinstance(integrations, list) and all(isinstance(i, dict) for i in integrations):
        check({i.get('id') for i in integrations} == {'mermaid', 'markitdown', 'n8n', 'firecrawl', 'plane'}, 'five planned integrations required')
        check(all(i.get('status') == 'planned' and i.get('enabled') is False for i in integrations), 'unimplemented integrations must stay disabled')
    else:
        errors.append('integrations must be an array of objects')
    for filename, required in [('tasks.csv', {'task_id', 'status', 'owner', 'due_date', 'source_ref'}), ('evidence.csv', {'evidence_id', 'claim_type', 'source_url', 'accessed_at'})]:
        try:
            with (plugin / 'assets/templates' / filename).open(encoding='utf-8', newline='') as f:
                rows = list(csv.reader(f))
            check(len(rows) == 1 and required <= set(rows[0]) and len(rows[0]) == len(set(rows[0])), f'{filename}: must be a header-only template with unique required fields')
        except (OSError, csv.Error) as exc:
            errors.append(f'{filename}: {exc}')
    for file in ('README.md', 'AGENTS.md', '.gitignore', 'tests/test_workspace.py'):
        check((root / file).is_file(), f'missing workspace file: {file}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        errors = validate(args.root)
    except (TypeError, AttributeError, KeyError, IndexError) as exc:
        errors = [f'malformed configuration: {exc}']
    if errors:
        print('\n'.join('ERROR: ' + e for e in errors))
        return 1
    print('PASS: 7 skills, manifests, marketplace, local links, templates and 5 disabled integration plans.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
