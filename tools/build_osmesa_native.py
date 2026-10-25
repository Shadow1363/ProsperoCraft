#!/usr/bin/env python3
"""Build pinned Mesa OSMesa/softpipe without game transformations.

Requires the graphics SDK/cross file produced by the existing Vulkan build.
This builds static components, not an installable PS5 app or a hardware GL driver.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PORT = ROOT / 'client/ports/opengl'


def fetch_verified(record, offline):
    path = ROOT / '.tools' / record['file']
    if not path.exists():
        if offline:
            raise FileNotFoundError(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + '.download')
        try:
            with urllib.request.urlopen(record['url'], timeout=90) as src, temporary.open('wb') as out:
                shutil.copyfileobj(src, out)
            verify(temporary, record)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    verify(path, record)
    return path


def verify(path, record):
    data = path.read_bytes()
    if len(data) != record['size'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError('Pinned archive mismatch: ' + str(path))


def build(host=False, offline=False):
    pin = json.loads((PORT / 'mesa-sources.json').read_text())
    archive = fetch_verified(pin['archive'], offline)
    dependencies = [fetch_verified(dep, offline) for dep in pin['dependencies']]
    patches = sorted(PORT.glob('*.patch'))
    identity = hashlib.sha256(archive.read_bytes() + b''.join(p.read_bytes() for p in patches)).hexdigest()
    source = ROOT / 'build/mesa-osmesa-source'
    stamp = source / '.source-sha256'
    if not stamp.exists() or stamp.read_text().strip() != identity:
        shutil.rmtree(source, ignore_errors=True)
        temporary = ROOT / 'build/osmesa-extract'
        shutil.rmtree(temporary, ignore_errors=True)
        temporary.mkdir(parents=True)
        with tarfile.open(archive) as tar:
            tar.extractall(temporary, filter='data')
        shutil.move(str(temporary / ('mesa-' + pin['version'])), source)
        shutil.rmtree(temporary)
        for patch in patches:
            subprocess.run(['git', 'apply', '--unsafe-paths', '--directory=' + str(source), str(patch)], check=True)
        stamp.write_text(identity + '\n')
    packagecache = source / 'subprojects/packagecache'
    packagecache.mkdir(exist_ok=True)
    for dep in dependencies:
        shutil.copyfile(dep, packagecache / dep.name)
    venv = ROOT / '.tools/graphics-python'
    env = dict(os.environ, PATH=str(venv / 'bin') + ':/opt/homebrew/opt/llvm/bin:' + os.environ['PATH'],
               LLVM_CONFIG='/opt/homebrew/opt/llvm/bin/llvm-config')
    out = ROOT / ('build/osmesa-host' if host else 'build/osmesa-ps5')
    options = [
        '--wrap-mode=nodownload', '-Ddefault_library=static', '-Dgallium-drivers=softpipe', '-Dvulkan-drivers=', '-Dplatforms=',
        '-Dglx=disabled', '-Degl=disabled', '-Dgbm=disabled', '-Dopengl=true', '-Dshared-glapi=disabled',
        '-Dgles1=disabled', '-Dgles2=disabled', '-Dosmesa=true', '-Dllvm=disabled', '-Dbuildtype=release',
        '-Dbuild-tests=false', '-Dvalgrind=disabled', '-Dlibunwind=disabled', '-Dzstd=disabled',
        '-Dzlib=enabled', '--force-fallback-for=zlib', '-Dexpat=disabled', '-Dxmlconfig=disabled',
        '-Dtools=', '-Dvideo-codecs=',
    ]
    if host:
        env.update(CC='clang', CXX='clang++')
    else:
        options += ['-Dps5-emulated-tls=true', '--cross-file', str(ROOT / 'build/graphics-cross.ini')]
    args = [str(venv / 'bin/meson'), 'setup']
    if (out / 'build.ninja').exists():
        build_stamp = out / '.source-identity'
        args += ['--reconfigure' if build_stamp.exists() and build_stamp.read_text().strip() == identity else '--wipe']
    subprocess.run(args + [str(out), str(source)] + options, env=env, check=True)
    (out / '.source-identity').write_text(identity + '\n')
    targets = ['src/gallium/targets/osmesa/libOSMesa.a', 'src/util/libxmlconfig.a', 'subprojects/zlib-1.3.1/libz.a']
    subprocess.run(['ninja', '-C', str(out), '-j4', *targets], env=env, check=True)
    extra_audit = {}
    if not host:
        llvm = Path('/opt/homebrew/opt/llvm/bin')
        merged = out / 'osmesa-raw.o'
        subprocess.run(['/opt/homebrew/opt/lld/bin/ld.lld', '-r', '--whole-archive',
                        *[str(out / name) for name in targets], '--no-whole-archive', '-o', str(merged)], check=True)
        nm = subprocess.check_output([str(llvm / 'llvm-nm'), '--undefined-only', str(merged)], text=True)
        undefined = sorted({line.split()[-1] for line in nm.splitlines() if line.strip()})
        if any(name.startswith(('OSMesa', '_glapi_', 'driQueryOption')) for name in undefined):
            raise ValueError('Unresolved internal Mesa API: ' + str(undefined))
        extra_audit = {'relocatable_sha256': hashlib.sha256(merged.read_bytes()).hexdigest(),
                       'unresolved_external_symbols': undefined,
                       'link_scope': 'Relocatable only; external SDK/provider bindings and ctor staging still required'}
    audit = {
        'source': pin, 'source_patch_identity': identity,
        'patches': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in patches},
        'archives': {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in targets},
        'host': host, **extra_audit,
        'scope': 'Real OSMesa/softpipe static components; no resident integration or PS5 acceptance yet',
    }
    (out / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', action='store_true')
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    print(build(args.host, args.offline))
