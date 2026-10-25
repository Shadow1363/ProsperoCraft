# Client_OpenGL_Provider

Frozen PPSA99874 01.000.029;human ALL5 PASS and matching session/startup reports on2026-10-25.

Three real Mesa softpipe/OpenGL JNI contexts verify192RGBA pixels and768guards,then DestroyJavaVM completes. This is software OpenGL bootstrap acceptance,not Minecraft startup,hardware GL or visible presentation. Vulkan remains the intended game renderer;server endurance stays deferred.

Tested source: `fd0434b89a97650d8b9b0efda40e43f2c100008e`. Full local ZIP SHA256: `ed0cc6f49528b44b6d131c800e3c6359d01e009ae52524b7e96262a71491b685`. See validation.json for exact pins,omissions,retained hashes and scope. Do not modify this snapshot;continue in root client/.

The app-only release omits54original game/Java JARs. Extract it and run the included provision_client_release.py with --manifest validation.json --app-dir PPSA99874 --jars-dir /path/to/verified/jars. It verifies retained files and every original JAR before provisioning.

The release includes matching OpenAL LGPL source/relink materials. Its unmodified relink reproduces the accepted native ELF;modified builds do not inherit console acceptance. Mesa original source/port patches and notices are in app assets.
