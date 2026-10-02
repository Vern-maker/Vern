"""Create a new Vern workspace from the public starter package."""
import argparse
import json
from pathlib import Path
import shutil
import sys


def initialize(target, package):
    if sys.version_info < (3, 10):
        raise ValueError('Python 3.10 or newer is required')
    target = Path(target).expanduser().resolve()
    package = Path(package).resolve()
    required = ['templates/AGENTS.template.md', 'templates/task-card.md',
                'templates/method-card.md', 'templates/review.md', 'scripts/search.py']
    for name in required:
        if not (package / name).is_file():
            raise ValueError('Incomplete starter package: ' + name)
    if target.exists():
        raise ValueError('Target already exists. Existing files are preserved; choose a new folder.')
    target.mkdir(parents=True, exist_ok=False)
    for folder in ('资料', '任务', '方法', '复盘', 'templates', 'tools'):
        (target / folder).mkdir()
    shutil.copyfile(package / 'templates/AGENTS.template.md', target / 'AGENTS.md')
    for name in ('task-card.md', 'method-card.md', 'review.md'):
        shutil.copyfile(package / 'templates' / name, target / 'templates' / name)
    shutil.copyfile(package / 'scripts/search.py', target / 'tools/search.py')
    (target / '资料/演示资料.md').write_text(
        '---\nstatus: example\n---\n# 演示资料\n\n这是一条演示记录，不是个人历史。\n'
        '演示规则：交付前核对任务目标、来源和完成标准。\n', encoding='utf-8')
    (target / 'README.md').write_text(
        '# Vern 工作空间\n\n资料：输入与证据。任务：目标与状态。方法：可复用做法。复盘：验收与改进。\n\n'
        '将此文件夹作为工作目录打开。先读取 AGENTS.md，用演示资料验证检索，再加入授权资料。\n'
        '脚本只建立本地文件，不会登录账户、发送资料、注册定时任务或自动调用模型。\n', encoding='utf-8')
    return target


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, help='A new workspace folder chosen by you')
    args = p.parse_args()
    try:
        target = initialize(args.root, Path(__file__).resolve().parents[1])
    except (ValueError, OSError) as exc:
        p.exit(2, str(exc) + '\n')
    print(json.dumps({'initialized': True, 'global_config_changed': False,
                      'automation_enabled': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
