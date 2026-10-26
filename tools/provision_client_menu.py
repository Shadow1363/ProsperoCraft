#!/usr/bin/env python3
"""Restore the pinned original JARs AND assets to a ProsperoCraft menu release."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request


def checked(path, row):
    if not path.is_file() or path.stat().st_size != row['bytes']:
        raise ValueError('Missing or incorrect size: ' + str(path))
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != row['sha256']:
        raise ValueError('SHA256 mismatch: ' + str(path))


def safe(root, relative):
    parts = PurePosixPath(relative)
    if parts.is_absolute() or '..' in parts.parts or '\\' in relative:
        raise ValueError('Unsafe manifest path')
    target = root.joinpath(*parts.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes app/cache')
    return target


def provision(record, app, jars=None, assets=None, cache=None, download=False):
    if record['format'] != 'prosperocraft-client-menu-1':
        raise ValueError('Menu-release manifest required')
    app = Path(app).resolve()
    for row in record['retained_files']:
        checked(safe(app, row['path']), row)
    # Resolve and verify every source before changing any application file.
    def source(row):
        base = jars if row['kind'] == 'jar' else assets
        if base:
            path = safe(Path(base).resolve(), row['source_path'])
            checked(path, row)
            return row, path
        if not cache:
            raise ValueError('Use --jars-dir/--assets-dir or --cache-dir with --download')
        path = safe(Path(cache).resolve(), row['kind'] + '/' + row['source_path'])
        if path.exists():
            checked(path, row)  # Corruption is an error, never silently accepted.
            return row, path
        if not download:
            raise ValueError('Missing cached original; use --download: ' + str(path))
        url = row['url']
        if not url.startswith(('https://piston-data.mojang.com/',
                               'https://libraries.minecraft.net/',
                               'https://resources.download.minecraft.net/')):
            raise ValueError('Unexpected publisher URL')
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    shutil.copyfileobj(response, output)
                output.close()
                checked(temporary, row)
                os.replace(temporary, path)
            finally:
                temporary.unlink(missing_ok=True)
        return row, path
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        sources = list(pool.map(source, record['excluded_files']))
    for row, path in sources:
        target = safe(app, row['path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output:
            temporary = Path(output.name)
            try:
                with path.open('rb') as stream:
                    shutil.copyfileobj(stream, output)
                output.close()
                checked(temporary, row)
                os.replace(temporary, target)
            finally:
                temporary.unlink(missing_ok=True)
    for row in record['retained_files'] + record['excluded_files']:
        checked(safe(app, row['path']), row)
    expected = {row['path'] for row in record['retained_files'] + record['excluded_files']}
    actual = {p.relative_to(app).as_posix() for p in app.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError('Reconstructed app contains unexpected or missing files')
    print('PASS exact app reconstruction:', len(sources), 'original JAR/asset files restored.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--app-dir', type=Path, required=True)
    parser.add_argument('--jars-dir', type=Path, help='Original pinned JAR directory')
    parser.add_argument('--assets-dir', type=Path, help='Original assets root containing objects/')
    parser.add_argument('--cache-dir', type=Path)
    parser.add_argument('--download', action='store_true', help='Fetch missing originals from pinned publisher URLs')
    args = parser.parse_args()
    provision(json.loads(args.manifest.read_text()), args.app_dir, args.jars_dir,
              args.assets_dir, args.cache_dir, args.download)


if __name__ == '__main__':
    main()
