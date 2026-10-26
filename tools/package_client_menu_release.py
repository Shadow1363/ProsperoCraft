#!/usr/bin/env python3
"""Derive an app-only menu release from accepted bytes without rebuilding."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TESTED = '26f31cc26bc960d3c7e35205c0280e8b83bc6e475a17b8383c778583cf952b88'


def package(full, output):
    with full.open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == TESTED, 'Exact accepted062 ZIP required'
    output.mkdir(parents=True, exist_ok=True)
    lock = json.loads((ROOT / 'client/26.3.lock.json').read_text())
    jars = {r['file']: r for r in lock['artifacts']}
    record = {'format': 'prosperocraft-client-menu-1', 'title_id': 'PPSA99874',
              'version': '01.000.062', 'tested_source_commit': 'f3349a1fb90a9304d7aa808b339bd37738607d14',
              'full_local_zip_sha256': TESTED, 'retained_files': [], 'excluded_files': []}
    public = output / 'ProsperoCraft-01.000.062-menu-app-only.zip'
    with zipfile.ZipFile(full) as source, zipfile.ZipFile(public, 'w', zipfile.ZIP_DEFLATED) as target:
        assert source.testzip() is None
        index = json.loads(source.read('PPSA99874/assets/java25/game-assets/indexes/34.json'))
        objects = {r['hash']: r['size'] for r in index['objects'].values()}
        jar_count = asset_count = 0
        for entry in source.infolist():
            if entry.is_dir():
                continue
            assert entry.filename.startswith('PPSA99874/')
            relative = entry.filename.removeprefix('PPSA99874/')
            data = source.read(entry)
            row = {'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            if relative.startswith('assets/java25/client/jars/'):
                name = Path(relative).name
                pin = jars[name]
                assert row['sha256'] == pin['sha256'] and row['bytes'] == pin['size']
                row.update(kind='jar', source_path=name, url=pin['url'])
                record['excluded_files'].append(row)
                jar_count += 1
            elif relative.startswith('assets/java25/game-assets/objects/'):
                digest = Path(relative).name
                assert hashlib.sha1(data).hexdigest() == digest and len(data) == objects[digest]
                row.update(kind='asset', source_path='objects/' + digest[:2] + '/' + digest,
                           url='https://resources.download.minecraft.net/' + digest[:2] + '/' + digest)
                record['excluded_files'].append(row)
                asset_count += 1
            else:
                # Only accepted app files: public ZIP never gains logs, saves or host files.
                target.writestr(entry, data)
                record['retained_files'].append(row)
        assert jar_count == len(jars) == 54 and asset_count == len(objects) == 5147
    (output / 'client062-install-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
    print('PASS public artifact derived from accepted bytes:', public, jar_count, 'JARs and', asset_count, 'assets excluded')
    return record


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--full-package', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    package(a.full_package, a.output)
