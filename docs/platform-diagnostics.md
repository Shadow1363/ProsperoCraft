# PS5 diagnostic compatibility

Starting in probe 01.000.012, the runtime includes the real OpenJDK management
library. Preflight queries heap/non-heap usage and actual VM input arguments;
loading the `ManagementFactory` class without initializing it is insufficient.
These values come from HotSpot's JMM interface, not substituted counters.

OSHI 6.9.0 has no PS5 operating-system or hardware backend. The port keeps the
accurate `os.name=PS5`. It does not select a desktop FreeBSD backend, invent
physical memory/CPU readings, or globally filter warnings. For Minecraft's
optional crash-report hardware/software telemetry, it records an explicit
unavailable-on-PS5 detail. JVM memory, flags, version, and other report entries
remain available. Full OSHI support is not implemented.

`tools/PreparePlatformDiagnostics.java` uses the host JDK 25 Class-File API to
wrap only `SystemReport.putHardware` and `putSoftware`. Each wrapper checks the
actual `os.name`; the original method is retained and called on other platforms.
The transform verifies the expected method descriptors and exactly two matches,
and the Class-File verifier validates the generated class.

The verified original `server-26.3.jar` is left intact. Signed Java packages cannot
contain a separately unsigned replacement class, so preparation creates a complete
**local unsigned diagnostic derivative**, `ps5-platform-diagnostics.jar`. It
also inserts one call to ServerGameplay25.tick(this) immediately before the final
return of MinecraftServer.tickServer. Every original instruction and method
remains intact; an opcode/invocation audit checks this. The helper samples
item-use and tick gaps, and build071 explicitly enables the user-requested
operator policy through vanilla PlayerList APIs on the server thread. It
preserves every other server class/resource byte-for-byte; the changed manifest
and removed signing metadata explicitly identify an unsigned derivative. No JVM
signature verification is disabled. Existing gameplay, registry, world generation,
network, authentication and save instructions remain unchanged. The tick hook
now also changes operator permissions by explicit policy, so it is not entirely
read-only. Authentication and whitelist enforcement remain enabled.

This is an adapted server runtime, not a claim that the executed server artifact
is Mojang's unmodified signed JAR. Both the original and generated class hashes
are recorded in `platform-diagnostics-audit.json`. The original 40 JARs remain
hash-verified in preflight. Generated game classes/JARs, including this derivative,
stay out of source commits and public binary release assets. Build them locally
from the pinned official input. The frozen Server_Bootstrap snapshot is unchanged.

Checks:

```sh
python3 tools/test_platform_diagnostics.py
python3 tools/test_server_probe.py --runtime-image /path/to/PS5_Homebrew/build/java25/boot-image
python3 tools/test_server_start.py
```

The diagnostic test compares the complete JAR contents, confirms original input
checksums, and exercises the PS5 report path under `-Xverify:all` on a host JVM.
The real host server start/save/stop regression uses the derivative's retained
desktop path. Target execution, management preflight, verifier memory fallback
and real server readiness/save/stop still require PS5 validation.
