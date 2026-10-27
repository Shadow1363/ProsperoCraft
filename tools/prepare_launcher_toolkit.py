#!/usr/bin/env python3
"""Reproduce a hash-checked, pinned subset of PS5_VKHomebrewUI; no sample app."""
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REV = '2188642afbcc8d84d36149124f3d9e39dc1b1a05'
URL = 'https://github.com/mihawk-99/PS5_VKHomebrewUI.git'

def prepare():
    source = ROOT / '.tools/PS5_VKHomebrewUI'
    if not source.exists():
        subprocess.run(['git', 'clone', URL, str(source)], check=True)
    subprocess.run(['git', '-C', str(source), 'cat-file', '-e', REV], check=True)
    dest = ROOT / 'client/launcher/toolkit'
    paths = subprocess.check_output(['git', '-C', str(source), 'ls-tree', '-r', '--name-only', REV], text=True).splitlines()
    selected = [p for p in paths if p.startswith(('src/gfx/', 'src/ui/', 'src/core/', 'src/audio/', 'assets/fonts/', 'third_party/fonts/', 'tools/compile-vk-shaders.sh', 'tools/bake-fonts.sh', 'tools/font-baker/', 'third_party/stb/stb_truetype.h', 'third_party/stb/LICENSE', 'src/platform/ps5/system.hpp', 'docs/')) or p in ('LICENSE', 'THIRD_PARTY_NOTICES.md', 'README.md', 'AGENTS.md')]
    # Keep reproduction docs, omit large gallery media and unused font source files.
    selected = [p for p in selected if not p.startswith('docs/media/') and not p.endswith('.ttf')]
    hashes = {}
    for p in selected:
        data = subprocess.check_output(['git', '-C', str(source), 'show', REV + ':' + p])
        target = dest / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        hashes[p] = hashlib.sha256(data).hexdigest()
    (dest / 'upstream.json').write_text(json.dumps({'repository': URL, 'revision': REV, 'patches': [], 'sha256': hashes}, indent=2) + '\n')
    return dest

if __name__ == '__main__':
    print(prepare())
