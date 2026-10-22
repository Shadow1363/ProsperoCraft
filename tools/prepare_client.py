#!/usr/bin/env python3
"""Stage pinned client Java artifacts; never substitute desktop natives for PS5."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def checked(path, record):
    data = path.read_bytes()
    if len(data) != record['size']:
        raise ValueError('Artifact size: ' + path.name)
    for algorithm in ['sha1', 'sha256']:
        if algorithm in record and hashlib.new(algorithm, data).hexdigest() != record[algorithm]:
            raise ValueError('Artifact ' + algorithm + ': ' + path.name)
    return data


def cached(cache, record, name, offline):
    path = cache / name
    if not path.exists():
        if offline:
            raise FileNotFoundError('Offline cache missing: ' + str(path))
        if not record['url'].startswith('https://'):
            raise ValueError('HTTPS artifact URL required')
        with tempfile.NamedTemporaryFile(dir=cache, delete=False) as output:
            temporary = Path(output.name)
            try:
                with urllib.request.urlopen(record['url'], timeout=60) as response:
                    shutil.copyfileobj(response, output)
                output.close()
                checked(temporary, record)
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
    checked(path, record)
    return path


def prepare(cache, destination, offline=False):
    lock = json.loads((ROOT / 'client/26.3.lock.json').read_text())
    cache, destination = Path(cache).resolve(), Path(destination).resolve()
    # Isolate client preparation from the working server's assets and packages.
    if destination != (ROOT / 'build/client').resolve():
        raise ValueError('Client destination must be this checkout\'s build/client')
    cache.mkdir(parents=True, exist_ok=True)
    metadata = cached(cache, lock['metadata'], '26.3.metadata.json', offline)
    official = json.loads(metadata.read_text())
    if official['id'] != lock['minecraft'] or official['javaVersion']['majorVersion'] != lock['java_major']:
        raise ValueError('Metadata identity mismatch')
    expected = {'minecraft:client:26.3': official['downloads']['client']}
    expected.update({row['name']: row['downloads']['artifact'] for row in official['libraries'] if not row.get('rules')})
    assert set(expected) == {row['id'] for row in lock['artifacts']}
    assert len({row['file'] for row in lock['artifacts']}) == len(lock['artifacts'])
    paths = []
    for row in lock['artifacts']:
        if Path(row['file']).name != row['file']:
            raise ValueError('Invalid artifact file name')
        for field in ['sha1', 'url', 'size']:
            if row[field] != expected[row['id']][field]:
                raise ValueError('Publisher metadata mismatch: ' + row['id'])
        path = cached(cache, row, row['file'], offline)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError('Invalid JAR: ' + row['file'])
        paths.append((row, path))
    for field in ['id', 'sha1', 'url', 'size']:
        if lock['asset_index'][field] != official['assetIndex'][field]:
            raise ValueError('Publisher asset-index mismatch')
    index = cached(cache, lock['asset_index'], lock['asset_index']['file'], offline)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='client-stage-', dir=destination.parent) as folder:
        stage = Path(folder)
        jars = stage / 'jars'; jars.mkdir()
        for row, path in paths:
            shutil.copyfile(path, jars / row['file'])
        (stage / 'client-inventory.properties').write_text(''.join(row['file'] + '=' + row['sha256'] + '\n' for row, _ in paths))
        shutil.copyfile(index, stage / 'assets-index-34.json')
        embedded = []
        for row, path in paths:
            with zipfile.ZipFile(path) as archive:
                resources = [name for name in archive.namelist() if name.endswith(('.so', '.dll', '.dylib', '.jnilib'))]
                if resources:
                    embedded.append({'file': row['file'], 'native_resource_count_by_suffix': len(resources)})
        audit = {'minecraft': lock['minecraft'], 'java_artifacts': len(paths), 'desktop_conditional_artifacts_staged': 0, 'asset_objects_downloaded': 0, 'project_game_transformations': [], 'embedded_native_resources_not_executed': embedded, 'native_bindings': 'PS5 port pending', 'console': 'pending; artifact preparation is not a client launch'}
        (stage / 'execution-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(stage, destination)
    print('Prepared', len(paths), 'verified client/Java JARs; zero conditional desktop artifacts. Asset objects, PS5 bindings and client launch pending.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path, default=ROOT / '.tools/client')
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    prepare(args.cache_dir, ROOT / 'build/client', args.offline)


if __name__ == '__main__':
    main()
