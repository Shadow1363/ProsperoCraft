#!/usr/bin/env python3
"""Restore exact upstream client JARs to the frozen app-only client milestone release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provision(record, app, jars):
    if record['milestone'] not in {'Client_Foundation', 'Client_Native_Loading', 'Client_LWJGL_Core'}:
        raise ValueError('Supported client milestone validation manifest required')
    app, jars = Path(app).resolve(), Path(jars).resolve()
    for row in record['retained_files']:
        path = app / row['path']
        if not path.is_file() or digest(path) != row['sha256']:
            raise ValueError('Retained app checksum: ' + row['path'])
    for row in record['excluded_jars']:
        if Path(row['file']).name != row['file']:
            raise ValueError('Invalid artifact name')
        source = jars / row['file']
        if not source.is_file() or digest(source) != row['sha256']:
            raise ValueError('Prepare matching original JAR first: ' + row['file'])
    target = app / 'assets/java25/client/jars'
    with tempfile.TemporaryDirectory(prefix='client-provision-', dir=app.parent) as folder:
        stage = Path(folder)
        for row in record['excluded_jars']:
            shutil.copyfile(jars / row['file'], stage / row['file'])
        target.mkdir(parents=True, exist_ok=True)
        for row in record['excluded_jars']:
            os.replace(stage / row['file'], target / row['file'])
    print('Restored', len(record['excluded_jars']), 'verified original client/Java JARs. No login or graphics launch attempted.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--app-dir', type=Path, required=True, help='Extracted PPSA99874 directory')
    parser.add_argument('--jars-dir', type=Path, required=True, help='Matching prepare_client.py output: build/client/jars')
    args = parser.parse_args()
    provision(json.loads(args.manifest.read_text()), args.app_dir, args.jars_dir)


if __name__ == '__main__':
    main()
