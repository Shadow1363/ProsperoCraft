# Client_STB_Codecs

Frozen PPSA99874 01.000.031;human ALL5 PASS and matching saved session on2026-10-25. The detailed startup download was incomplete;per-cycle fields come from the accepted fixture,not separately retrieved detailed output.

The five checks cover real STB PNG encode/file-read/decode/free cycles,768exact RGBA bytes/384input guards,truncated PNG and invalid Vorbis controls,Perlin/native structs and JVM shutdown. This does not establish valid Vorbis decoding,font/resize/DXT/callback coverage or Minecraft startup. Server endurance stays deferred.

Tested source:`4dd4ef83ab5bc1609dcf3a4b333fb1bbb65298e6`. Full local ZIP SHA256:`061d1ab8b40fcd90cf5e3854ee6d5220a7410685ddb69634faaf688db92cb42c`. See validation.json for pins,omissions and retained hashes. Preserve this snapshot;continue in root client/.

The app-only release omits54original game/Java JARs. Extract it and use the included provision helper with --manifest validation.json --app-dir PPSA99874 --jars-dir /path/to/verified/jars. All retained files and JARs are checked.

The matching OpenAL LGPL source/relink kit reproduces the exact accepted native ELF. Source edits do not inherit console acceptance. Original STB sources/notices are included in app assets.
