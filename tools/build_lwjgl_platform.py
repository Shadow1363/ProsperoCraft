#!/usr/bin/env python3
"""Build the explicit PS5 platform dependency port from pinned LWJGL sources."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    portdir = ROOT / 'client/ports/lwjgl'
    port = json.loads((portdir / 'port.json').read_text())
    lock = json.loads((ROOT / 'client/26.3.lock.json').read_text())
    original = next(row for row in lock['artifacts'] if row['id'] == port['upstream_binary_id'])
    annotation = next(row for row in lock['artifacts'] if row['id'].startswith('org.jspecify:jspecify:'))
    cache = ROOT / '.tools/client'
    for row in [original, annotation]:
        if sha((cache / row['file']).read_bytes()) != row['sha256']:
            raise ValueError('Prepare verified original client artifacts first: ' + row['file'])
    record = port['source_archive']; sourcejar = cache / record['file']
    if not sourcejar.exists():
        if args.offline:
            raise FileNotFoundError('Source archive missing from offline cache')
        with urllib.request.urlopen(record['url'], timeout=60) as response:
            data = response.read()
        if len(data) != record['size'] or sha(data) != record['sha256']:
            raise ValueError('LWJGL source download checksum')
        sourcejar.write_bytes(data)
    data = sourcejar.read_bytes()
    if len(data) != record['size'] or sha(data) != record['sha256']:
        raise ValueError('LWJGL source checksum')
    out = ROOT / 'build/client-ports/lwjgl';out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lwjgl-build-', dir=out) as folder:
        work = Path(folder); sources = work / 'sources'; sources.mkdir(); classes = work / 'classes'; classes.mkdir()
        with zipfile.ZipFile(sourcejar) as archive:
            for name in port['source_units']:
                destination = sources / name; destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(name))
        for patch in port['patches']:
            subprocess.run(['git', 'apply', '--unsafe-paths', '--directory=' + str(sources), str(portdir / patch)], check=True)
        cp = ':'.join(str(cache / row['file']) for row in [original, annotation])
        subprocess.run([str(args.java_home / 'bin/javac'), '--release', '8', '-proc:none', '-cp', cp, '-d', str(classes), *[str(sources / name) for name in port['source_units']]], check=True)
        replacements = {str(path.relative_to(classes)): path.read_bytes() for path in classes.rglob('*.class')}
        if not replacements or not all(name.startswith(('org/lwjgl/system/Platform', 'org/lwjgl/system/APIUtil')) for name in replacements):
            raise ValueError('Unexpected dependency compilation output')
        destination = out / port['output']
        with zipfile.ZipFile(cache / original['file']) as base, zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as result:
            for entry in base.infolist():
                if entry.filename not in replacements:
                    result.writestr(entry, base.read(entry.filename))
            for name, payload in sorted(replacements.items()):
                entry = zipfile.ZipInfo(name);entry.compress_type = zipfile.ZIP_DEFLATED;result.writestr(entry, payload)
            entry = zipfile.ZipInfo('META-INF/PS5-PORT-LICENSE.txt');entry.compress_type = zipfile.ZIP_DEFLATED
            result.writestr(entry, (portdir / 'LICENSE.md').read_bytes())
        with zipfile.ZipFile(cache / original['file']) as base, zipfile.ZipFile(destination) as result:
            if result.testzip() is not None:
                raise ValueError('Port JAR integrity')
            for name in base.namelist():
                if name not in replacements and result.read(name) != base.read(name):
                    raise ValueError('Unexpected upstream delta: ' + name)
        audit = {'original_sha256': original['sha256'], 'output_sha256': sha(destination.read_bytes()), 'source_sha256': record['sha256'], 'recompiled_classes': sorted(replacements), 'patch_sha256': {name: sha((portdir / name).read_bytes()) for name in port['patches']}, 'game_jar_modified': False, 'activated_for_game': False, 'console': 'pending; dependency platform identification only; native loading unported'}
        (out / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
        print('Built', destination, 'SHA256', audit['output_sha256'])


if __name__ == '__main__':
    main()
