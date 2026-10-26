# Client067 — real PS5 speaker output candidate

The user confirms066is fast and the world playable,with roughly30secondstartup.
The exact066build is now a full GitHub release and independently preserved.
067keeps those C1,input,heap,renderer and game settings while adding audio.
It is a development candidate,not a new accepted audio release.

## Mixer to AudioOut

A new `ps5` OpenAL Soft playback backend opens **PS5 Speakers** through the existing
project's AudioOut ABI profile:SYSTEMuser0xff,mainport,48kHz,stereoS16,256frames.
Open/init happen before its mixing thread starts. The real OpenAL mixer renders
interleaved PCM;`sceAudioOutOutput` provides hardware pacing. No alternate game
sound engine,loopback diversion,pre-recorded soundtrack or fake success is used.

The buffer remains owned/aligned until the thread exits. Stop joins before drain
and close. Output errors are logged and mark the OpenAL device disconnected;
init/open failures return actual OpenAL errors. There is no capture/microphone,
surround,haptics or route-switching acceptance. A first submitted PCM block is
logged,which establishes API submission,not human-audible sound.

The original pinned OpenAL source/archive remains intact. A private archive
replaces the existing alc/helpers units and adds the newbackend unit;original
null/loopback implementations remain. Startup's private getenv binding defaults
`ALSOFT_DRIVERS` to `ps5`,honors a nonemptyexplicitoverride,and leaves process/global
getenv unchanged. Existing explicitlocalpath fallback and bounded native diagnostics
remain. Backend config/source/object hashes are recorded in the packaged audit.

## Volume migration

Earlier harness-created options muted master/music. On the first067launch,the
harness copies the existing options to `options.before-audio067.txt` if changes
are needed,then changes zero master/music defaults to **0.5/0.25**. Nonzero custom
volumes and other option bytes are retained. An obsolete `"No Output"` device
selection is cleared to the game's default;other chosen devices are preserved.
An `audio-enabled-067.txt` marker prevents later launches from overriding a user
who mutes again. This is supported options configuration,no game code hook.

## Checks

Host testing builds the actual pinned OpenAL with the PS5backend and fault-controlled
AudioOut calls. A real44.1kHz mono440Hzsource is resampled/mixed into nonzero48kHz
stereoS16PCM;channel balance,alignment,threeopen/context/closecycles,pause/resume,
initialization lifetime,init/open failures and output-disconnect are checked.
The newbackend/testsink/driver are instrumented withASan/UBSan. These calls are
host fixtures,not PS5audio emulation or audible-console acceptance.

The actual one-time Javaoptions migration is tested for legacy zeros,olddevice,
CRLF/customvaluepreservation,exactbackup,newprofiles and lateruser muting.
Existingstartup/OpenALconfig/target/fullpackagechecks verify the unchanged54
originalJARs,5,147assets,C1gate/input/heap and preserved066acceptedpackage.

## PS5 test

Install067,pressXonce,andlistenfor menu selection sounds/music and world sounds.
Try footsteps,punching/breaking blocks,nearbyentities and left/right changes with
camera orientation. Check that audio and play remain smooth and that pausing/
returning to menus does not crash. Existing options are backed up;use the game's
sound settings to adjust volume after the first migration. Some music begins
only after a delay. No prerecorded startup beep is added as a substitute for game
sound. If silent or unstable,reopenwithoutXandretainreports;native stderr contains
AudioOutinit/open/firstPCM/outputfailure/drain/close records. Speaker audibility,
channel balance,latency,pops/clicks,pause/reopen and long-duration behavior all need
actualPS5validation. Full save/reload/endurance and controller polish remain pending.

The public release stays066withoutaudio. A future067audio release needs exact
acceptedbinaryscope,updatedOpenALsource/relinkkitincludingnewbackend/source/CMake
recipe,completeoriginalfileprovisioning/notices/checks andverifieddownloads.
NoStoreworkisrequested. Waitforfurtheruserdirectionaftersoundcandidatevalidation.

The local corresponding-source kit check also rebuilds all190OpenALtargetsteps,
including the new PS5 backend, and links that replacement with the original shim.
The preserved-input relink exactly reproduces the candidate ELF. The fresh source
replacement differs and has no transferred console acceptance; neither check
establishes audible sound. No067public release kit has been published.
