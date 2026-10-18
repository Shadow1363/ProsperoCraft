#!/usr/bin/env python3
"""Host validation of the actual pinned update_tags codec and allocator settings."""
from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1];jdk=Path('/opt/homebrew/opt/openjdk@25/bin')
assets=root/'build/assets/java25/jars';lock=json.loads((root/'server/26.3.lock.json').read_text())
cp=':'.join([str(assets/'ps5-server-probe.jar'),str(assets/'ps5-platform-diagnostics.jar'),*[str(assets/r['file']) for r in lock['jars'] if r['file']!='server-26.3.jar']])
classes=root/'build/network-memory-test';classes.mkdir(exist_ok=True)
subprocess.run([str(jdk/'javac'),'-cp',cp,'-d',str(classes),str(root/'tools/test_tag_packet.java')],check=True)
run=[str(jdk/'java'),'-Xint','-Xmx144m','-Xss512k','-Dio.netty.allocator.type=unpooled','-cp',str(classes)+':'+cp,'test_tag_packet']
subprocess.run(run,check=True,timeout=90)
