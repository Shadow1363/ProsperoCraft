#!/usr/bin/env python3
"""Restore hash-pinned, locally prepared JARs to an extracted app-only release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provision(manifest, flavor, app_dir, jars_dir, player):
    if not re.fullmatch(r'[A-Za-z0-9_]{3,16}', player):
        raise ValueError('Supply your Minecraft account name (3–16 letters/digits/underscores)')
    record = next(row for row in manifest['builds'] if row['flavor'] == flavor)
    app_dir, jars_dir = Path(app_dir).resolve(), Path(jars_dir).resolve()
    # Validate every retained byte and every source before modifying the app.
    for row in record['retained_files']:
        path = app_dir / row['path']
        if not path.is_file() or digest(path) != row['sha256']:
            raise ValueError('Retained app checksum: ' + row['path'])
    for row in record['excluded_jars']:
        source = jars_dir / row['file']
        if not source.is_file() or digest(source) != row['sha256']:
            raise ValueError('Prepare matching upstream JAR first: ' + row['file'])
    target = app_dir / 'assets/java25/jars'
    with tempfile.TemporaryDirectory(prefix='ps5-release-', dir=app_dir.parent) as folder:
        stage = Path(folder)
        for row in record['excluded_jars']:
            shutil.copyfile(jars_dir / row['file'], stage / row['file'])
        target.mkdir(parents=True, exist_ok=True)
        for row in record['excluded_jars']:
            os.replace(stage / row['file'], target / row['file'])
    (app_dir / 'assets/java25/join-player.txt').write_text(player + '\n')
    print('Provisioned', flavor, record['app_version'], 'with', len(record['excluded_jars']), 'verified JARs and local account configuration')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--flavor', choices=['fabric', 'paper'], required=True)
    parser.add_argument('--app-dir', type=Path, required=True, help='Extracted PPSA99874 directory')
    parser.add_argument('--jars-dir', type=Path, required=True, help='Matching prepare_server.py output: build/assets/java25/jars')
    parser.add_argument('--join-player', required=True)
    args = parser.parse_args()
    provision(json.loads(args.manifest.read_text()), args.flavor, args.app_dir, args.jars_dir, args.join_player)


if __name__ == '__main__':
    main()
