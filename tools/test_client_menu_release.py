#!/usr/bin/env python3
"""Check real062 reconstruction, corruption refusal and publisher provisioning."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
from provision_client_menu import provision

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--release-dir', type=Path, required=True)
a = p.parse_args()
release = a.release_dir.resolve()
record = json.loads((release / 'client062-install-manifest.json').read_text())
assert len([r for r in record['excluded_files'] if r['kind'] == 'jar']) == 54
assert len([r for r in record['excluded_files'] if r['kind'] == 'asset']) == 5147
with tempfile.TemporaryDirectory(prefix='client062-release-check-', dir=ROOT / 'build') as folder:
    folder = Path(folder)
    with zipfile.ZipFile(release / 'ProsperoCraft-01.000.062-menu-app-only.zip') as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {'PPSA99874/' + r['path'] for r in record['retained_files']}
        assert not any('/client/jars/' in n or '/game-assets/objects/' in n for n in z.namelist())
        z.extractall(folder)
    app = folder / 'PPSA99874'
    # Actual accepted files, not synthetic app fixtures.
    provision(record, app, ROOT / 'build/client/jars', ROOT / 'build/client-assets')
    with zipfile.ZipFile(ROOT / 'dist/client-startup/PPSA99874.zip') as original:
        actual = {p.relative_to(app).as_posix() for p in app.rglob('*') if p.is_file()}
        expected = {n.removeprefix('PPSA99874/') for n in original.namelist() if not n.endswith('/')}
        assert actual == expected
        for relative in sorted(expected):
            assert (app / relative).read_bytes() == original.read('PPSA99874/' + relative), relative
    print('PASS reconstructed app matches every byte/file of the PS5 menu-confirmed full package')
    shutil.rmtree(app)
    # Exercise the real publisher download/cache branch on one actual JAR and asset.
    selected = [min((r for r in record['excluded_files'] if r['kind'] == kind and r['bytes']), key=lambda r: r['bytes']) for kind in ['jar', 'asset']]
    small = dict(record, retained_files=[], excluded_files=selected)
    app.mkdir()
    cache = folder / 'cache'
    provision(small, app, cache=cache, download=True)
    print('PASS actual pinned publisher JAR+asset downloads and cache verification')
    for kind in ['jar', 'asset']:
        row = next(r for r in selected if r['kind'] == kind)
        path = cache / kind / row['source_path']
        data = path.read_bytes()
        path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        before = {p.relative_to(app).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in app.rglob('*') if p.is_file()}
        try:
            provision(small, app, cache=cache, download=True)
        except ValueError as error:
            assert 'SHA256 mismatch' in str(error), str(error)
        else:
            raise AssertionError('Corrupt ' + kind + ' accepted')
        after = {p.relative_to(app).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in app.rglob('*') if p.is_file()}
        assert before == after, 'App mutated before source verification completed'
        path.write_bytes(data)
    retained = selected[0].copy()
    retained.pop('kind'); retained.pop('source_path'); retained.pop('url')
    damaged = app / retained['path']
    damaged.write_bytes(b'x' * retained['bytes'])
    try:
        provision(dict(small, retained_files=[retained]), app, cache=cache)
    except ValueError as error:
        assert 'SHA256 mismatch' in str(error)
    else:
        raise AssertionError('Changed retained binary accepted')
    print('PASS corrupted JAR, asset and retained-file refusal; no preflight app mutation')
