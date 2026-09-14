#!/usr/bin/env python3
"""Small local workspace and evidence ledger. No network or background actions."""
import argparse
from contextlib import contextmanager
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile

FIELDS = {'id', 'revision', 'title', 'goal', 'domain', 'status', 'phase', 'outcome',
          'decision', 'next_action', 'baseline', 'expected_change', 'cost',
          'review_on', 'evidence', 'history'}
TERMINAL = {'completed', 'stopped'}
PHASES = ['judged', 'ready', 'acted', 'feedback']
STARTER = ['AGENTS.md', 'SOURCE_OF_TRUTH.md', '方向.md', 'AI伙伴.md', 'README.md',
           '.gitignore', '资料/README.md']


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def inside(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError('Use a relative path inside this workspace')
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('Symlinks are not supported for managed files')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes workspace')
    return path


def atomic_text(path, text):
    if path.is_symlink():
        raise ValueError('Refusing a symlink output')
    fd, name = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(text)
        os.chmod(name, 0o600)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)  # Owned incomplete temporary output only.


def save(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def require_root(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError('An initialized workspace directory is required')
    marker = inside(root, '.zane-workbench.json')
    if load(marker) != {'format': 'zane-workbench', 'version': 1}:
        raise ValueError('Unknown workspace format; use existing-system adaptation')
    for folder in ['事项', '资料', '.history']:
        if not inside(root, folder).is_dir():
            raise ValueError('Missing managed directory: ' + folder)


@contextmanager
def locked(root):
    require_root(root)
    path = inside(root, '.write-lock')
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        raise ValueError('Another writer or stale lock exists; inspect before retrying')
    try:
        yield
    finally:
        path.rmdir()


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value):
        raise ValueError('Invalid case ID')
    return value


def validate(event, root):
    if not isinstance(event, dict) or set(event) != FIELDS:
        raise ValueError('Unexpected or missing case fields')
    identifier(event['id'])
    if type(event['revision']) is not int or event['revision'] < 1:
        raise ValueError('Revision must be a positive integer')
    for key in ['title', 'goal', 'domain', 'decision', 'baseline', 'expected_change', 'cost']:
        if not isinstance(event[key], str) or not event[key].strip():
            raise ValueError('Non-empty text required: ' + key)
    if not isinstance(event['next_action'], str):
        raise ValueError('next_action must be text')
    if event['status'] not in {'active', 'waiting', *TERMINAL} or event['phase'] not in PHASES:
        raise ValueError('Invalid state or evidence phase')
    if event['outcome'] not in {'unknown', 'partial', 'met', 'not_met'}:
        raise ValueError('Invalid outcome')
    if event['review_on'] is not None:
        date.fromisoformat(event['review_on'])
    if not isinstance(event['evidence'], list) or not event['evidence']:
        raise ValueError('At least one source-backed evidence entry is required')
    kinds = set()
    for item in event['evidence']:
        if not isinstance(item, dict) or set(item) != {'kind', 'text', 'source', 'at'}:
            raise ValueError('Invalid evidence shape')
        if item['kind'] not in {'input', 'action', 'feedback', 'correction'}:
            raise ValueError('Invalid evidence kind')
        if not isinstance(item['text'], str) or not item['text'].strip():
            raise ValueError('Evidence text is required')
        date.fromisoformat(item['at'])
        source = inside(root, item['source'])
        if not source.is_file():
            raise ValueError('Evidence source is missing')
        kinds.add(item['kind'])
    if not isinstance(event['history'], list):
        raise ValueError('History must be a list')
    if event['phase'] == 'acted' and 'action' not in kinds:
        raise ValueError('Acted phase requires action evidence')
    if event['phase'] == 'feedback' and 'feedback' not in kinds:
        raise ValueError('Feedback phase requires feedback evidence')
    if event['status'] == 'waiting' and (event['phase'] not in {'acted', 'feedback'} or 'action' not in kinds):
        raise ValueError('Waiting requires an actual action')
    if event['outcome'] == 'met' and (event['phase'] != 'feedback' or 'feedback' not in kinds):
        raise ValueError('A met goal requires observed feedback')
    if event['status'] in TERMINAL and (event['next_action'] or event['review_on'] is not None):
        raise ValueError('Terminal cases must not retain pending actions or review dates')
    return event


def all_cases(root):
    cases = []
    for path in sorted(inside(root, '事项').glob('*.json')):
        path = inside(root, str(path.relative_to(root)))
        event = validate(load(path), root)
        if path.stem != event['id']:
            raise ValueError('Case ID and filename differ')
        cases.append(event)
    return cases


def render(root):
    cases = all_cases(root)
    rows = ['# 现在做什么', '', '点击事项查看当前进展与下一步。', '',
            '| 事项 | 领域 | 状态 | 证据阶段 | 核实提示 |', '|---|---|---|---|---|']
    for event in cases:
        if event['status'] in TERMINAL:
            continue
        due = event['review_on'] and event['review_on'] <= date.today().isoformat()
        # No titles, next actions, quotes or costs in the default overview.
        domain = event['domain'].replace('|', '／').replace('\n', ' ')
        rows.append('| [{0}](事项/{0}.json) | {1} | {2} | {3} | {4} |'.format(
            event['id'], domain, event['status'], event['phase'], '日期已到，请核实' if due else ''))
    if len(rows) == 6:
        rows += ['', '从当前要推进的一件事开始。']
    atomic_text(inside(root, '现在做什么.md'), '\n'.join(rows) + '\n')


def initialize(root, mode="life", minimal=False):
    if minimal and mode != 'life':
        raise ValueError('Minimal startup is supported for life mode')
    if mode not in {'work', 'life', 'career'}:
        raise ValueError('Unknown workbench mode')
    if root.exists() or root.is_symlink():
        raise ValueError('Target already exists; adapt it without overwriting')
    if not root.parent.is_dir():
        raise ValueError('Choose an existing parent directory')
    source = Path(__file__).resolve().parents[1] / 'assets' / 'starter'
    profile = source.parent / ('life-minimal' if minimal else mode)
    if not profile.is_dir() or not (profile / 'AGENTS.md').is_file():
        raise ValueError('Missing workbench profile; reinstall the complete suite')
    root.mkdir(mode=0o700)
    for folder in ['事项', '资料', '.history']:
        (root / folder).mkdir(mode=0o700)
    selected = ['.gitignore', '资料/README.md'] if minimal else STARTER
    for relative in selected:
        path = inside(source, relative)
        atomic_text(root / relative, path.read_text(encoding='utf-8'))
    for src in sorted(profile.rglob('*')):
        if src.is_file():
            rel = src.relative_to(profile)
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_text(target, src.read_text(encoding='utf-8'))
    save(root / '.zane-workbench.json', {'format': 'zane-workbench', 'version': 1})
    render(root)


def add(root, event):
    with locked(root):
        validate(event, root)
        if event['revision'] != 1 or event['history']:
            raise ValueError('New cases start at revision 1 with empty history')
        path = inside(root, '事项/' + identifier(event['id']) + '.json')
        if path.exists():
            raise ValueError('Case exists; use revision-checked update')
        save(path, event)
        render(root)


def update(root, case_id, revision, patch, reason):
    if not reason.strip() or not isinstance(patch, dict):
        raise ValueError('A reason and an object patch are required')
    if set(patch) - (FIELDS - {'id', 'revision', 'history'}):
        raise ValueError('Cannot patch identity, revision, history or unknown fields')
    with locked(root):
        path = inside(root, '事项/' + identifier(case_id) + '.json')
        old = validate(load(path), root)
        if old['revision'] != revision:
            raise ValueError('Revision conflict; read current case before updating')
        new = {**old, **patch, 'revision': revision + 1}
        previous = old['evidence']
        if not isinstance(new['evidence'], list) or new['evidence'][:len(previous)] != previous:
            raise ValueError('Evidence is append-only; add a correction')
        added_kinds = {e.get('kind') for e in new['evidence'][len(previous):] if isinstance(e, dict)}
        if old['status'] in TERMINAL and new['status'] not in TERMINAL:
            raise ValueError('Create a linked new case instead of reopening a terminal case')
        delta = PHASES.index(new['phase']) - PHASES.index(old['phase']) if new['phase'] in PHASES else 0
        if delta > 0 and new['phase'] in {'acted', 'feedback'}:
            needed = {'acted': 'action', 'feedback': 'feedback'}[new['phase']]
            if needed not in added_kinds:
                raise ValueError('Phase advancement requires new corresponding evidence')
        if delta < 0 and 'correction' not in added_kinds:
            raise ValueError('Phase correction requires new correction evidence')
        if added_kinds & {'feedback', 'correction'} and not {'decision', 'outcome'} <= patch.keys():
            raise ValueError('Update current decision and outcome alongside feedback/correction')
        new['history'] = old['history'] + [{'at': stamp(), 'reason': reason, 'from_revision': revision}]
        validate(new, root)
        backup = inside(root, '.history/' + case_id + '-r' + str(revision) + '.json')
        if backup.exists():
            raise ValueError('Backup already exists; inspect before updating')
        save(backup, old)
        save(path, new)
        render(root)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['init', 'add', 'update', 'show', 'render', 'check']:
        p = sub.add_parser(command)
        p.add_argument('--root', type=Path, required=True)
        if command == 'init':
            p.add_argument('--mode', choices=['work', 'life', 'career'], default='life')
            p.add_argument('--minimal', action='store_true')
        if command == 'add':
            p.add_argument('--file', type=Path, required=True)
        if command in {'update', 'show'}:
            p.add_argument('--id', required=True)
        if command == 'update':
            p.add_argument('--expect-revision', type=int, required=True)
            p.add_argument('--patch', type=Path, required=True)
            p.add_argument('--reason', required=True)
    args = parser.parse_args()
    root = args.root.expanduser().absolute()
    try:
        if args.command == 'init':
            initialize(root, args.mode, args.minimal)
        else:
            require_root(root)
            if args.command == 'add':
                add(root, load(args.file))
            elif args.command == 'update':
                update(root, args.id, args.expect_revision, load(args.patch), args.reason)
            elif args.command == 'show':
                item = validate(load(inside(root, '事项/' + identifier(args.id) + '.json')), root)
                print(json.dumps(item, ensure_ascii=False, indent=2))
                return
            elif args.command == 'check':
                print('PASS: {} cases; source structure checked, facts not independently verified'.format(len(all_cases(root))))
                return
            else:
                with locked(root):
                    render(root)
        print('OK: ' + args.command)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, 'Stopped: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
