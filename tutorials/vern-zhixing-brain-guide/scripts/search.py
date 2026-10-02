"""Read-only literal search of Markdown records in a Vern workspace."""
import argparse
import json
from pathlib import Path
import re
import sys

AREAS = ('资料', '任务', '方法', '复盘')
INACTIVE = {'superseded', 'rejected', 'archived', '已失效', '已废弃'}


def search(root, query, limit=5):
    root = Path(root).resolve()
    if not query.strip():
        raise ValueError('Query must not be empty')
    if not 1 <= limit <= 20:
        raise ValueError('Limit must be between 1 and 20')
    if not root.is_dir():
        raise ValueError('Workspace does not exist')
    matches, warnings = [], []
    for area in AREAS:
        directory = root / area
        if not directory.is_dir() or directory.is_symlink():
            continue
        for path in sorted(directory.rglob('*.md')):
            if path.is_symlink() or any(part.startswith('.') for part in path.relative_to(root).parts):
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                continue
            try:
                text = path.read_text(encoding='utf-8-sig')
            except (OSError, UnicodeError):
                warnings.append(path.relative_to(root).as_posix())
                continue
            header = re.match(r'\A---\s*\n(.*?)\n---(?:\s*\n|$)', text, re.S)
            status = 'unspecified'
            if header:
                item = re.search(r'^status:\s*([^\n]+)', header.group(1), re.M)
                if item:
                    status = item.group(1).strip().strip('\"\'')
            if status in INACTIVE:
                continue
            lines = text.splitlines()
            hits = [(i + 1, line.strip()) for i, line in enumerate(lines) if query.casefold() in line.casefold()]
            if query.casefold() in path.stem.casefold() or hits:
                line, excerpt = hits[0] if hits else (1, path.stem)
                matches.append({'path': path.relative_to(root).as_posix(), 'line': line,
                                'status': status, 'excerpt': excerpt[:160]})
    return {'query': query, 'match_count': len(matches), 'matches': matches[:limit],
            'warnings': warnings, 'mode': 'literal-read-only'}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True)
    p.add_argument('--query', required=True)
    p.add_argument('--limit', type=int, default=5)
    args = p.parse_args()
    try:
        result = search(args.root, args.query, args.limit)
    except ValueError as exc:
        p.exit(2, str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
