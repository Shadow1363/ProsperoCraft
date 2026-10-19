# Build078 verification failure and079repair

The current078run fails without a reported process crash. All40official JAR
SHA256checks complete. The next check reads the official server Main.class
through JarFile and receives ExceptionInInitializerError. The old preflight
wrapper omits its nested cause. This is not a captured JAR checksum mismatch.
Native trace confirms a1000498byte module-image index copy.

The native0099index-only reader is incompatible with Java BasicImageReader's
64bitdefault MAP_ALL=true. Java omits the channel and attempts to slice resource
content beyond the shared index. Native-only resource tests missed this handoff.
Runtime0100uses the Java index/channel path on PS5, even if map.all=true, and
leaves desktop behavior unchanged.079also retains up to8nested preflight causes.

The host regression compiles the actualJava/native/ZIP/JNIreader sources. A
test-only registration opens the realimage and invokes the actualNativeImageBuffer
entry under a renamed binding; it does not substitute a map or decompressor.
OldJavaMAP_ALLbehavior reproduces the initializer failure during the exact
JarFileinput-stream operation. The nested hostcause is a Unicode NFKC resource
buffer-limit exception. That exact consolecause is inferred, not recorded in078.

The fixedPS5mode reader, including forcedmap.all=true, passes JarFile/server
bytecode checks and exactObject/Unicode/HTTPS/DTLS/JFRresource identity. A desktop
control uses ordinary hostJNI and also passes. Native ASan/UBSan and target
Java/native rebuild pass. These are hostchecks, not console acceptance.

079retains index-onlymemorysavings/allmodules/176MiBheap/NewRatio15/C1/world/view/
player/OP/security/timerfromDone settings and the existing game derivative.
No game transformation/replacement is added. Pending: actualPS5verification,
startup, resource-readlatency/nativeheadroom duringjoinedplay, playerpersistence,
mob/damage/GCstutter, full7200seconds and20playercapacity. Frozen058is unchanged.
