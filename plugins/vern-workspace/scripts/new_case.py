#!/usr/bin/env python3
"""Create a case folder with blank templates. Never overwrite an existing case."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

RESERVED = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)), *(f'lpt{i}' for i in range(1, 10))}


def create_case(root: Path, name: str) -> Path:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name in RESERVED:
        raise ValueError('Use 1-64 lowercase letters/digits with single hyphens; Windows device names are not allowed.')
    templates = Path(__file__).resolve().parents[1] / 'assets' / 'templates'
    files = ('brief.md', 'tasks.csv', 'evidence.csv')
    for file in files:
        if not (templates / file).is_file():
            raise FileNotFoundError(f'Missing packaged template: {file}')
    root = root.expanduser().resolve()
    destination = root / name
    if not destination.resolve().is_relative_to(root):
        raise ValueError('Case path escapes the requested root.')
    root.mkdir(parents=True, exist_ok=True)
    destination.mkdir(exist_ok=False)
    for folder in ('inputs', 'work', 'outputs'):
        (destination / folder).mkdir()
    for file in files:
        shutil.copyfile(templates / file, destination / file)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--root', type=Path, default=Path('cases'), help='Explicit case workspace; defaults to ./cases')
    args = parser.parse_args()
    try:
        result = create_case(args.root, args.name)
    except (OSError, ValueError) as exc:
        print(f'Case not created completely: {exc}', file=sys.stderr)
        return 1
    print(f'Created blank case: {result}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
