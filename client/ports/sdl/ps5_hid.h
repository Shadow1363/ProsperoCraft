/* SPDX-License-Identifier: GPL-3.0-or-later
 * PS5 keyboard/mouse ABI follows public device-tested HID layouts documented by
 * ZiZc3/Ruffle-Flash-PS5 src/hid.rs, commit1265f473e7479d6c0fcfb78cc160a0eea446bb08.
 * This driver is implemented here; no desktop HID emulation or LAN relay.
 */
#pragma once
#include <stdint.h>
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
struct prospero_keyboard_packet {uint64_t time;uint8_t intercepted,reserved0[7],connected,reserved1[3];int32_t length;uint32_t leds,modifiers;uint16_t keys[16];uint8_t reserved2[32];};
struct prospero_mouse_packet {uint64_t time;uint8_t connected,reserved0[3];uint32_t buttons;int32_t x,y,wheel,tilt;uint8_t reserved1[8];};
void prospero_hid_preload(void);
int prospero_hid_open(int mouse,int index);
int prospero_hid_read(int mouse,int handle,void *packets,int count);
void prospero_hid_close(int mouse,int handle);
#ifdef __cplusplus
}
static_assert(sizeof(prospero_keyboard_packet)==96);
static_assert(sizeof(prospero_mouse_packet)==40);
#else
_Static_assert(sizeof(struct prospero_keyboard_packet)==96,"PS5 keyboard ABI");
_Static_assert(sizeof(struct prospero_mouse_packet)==40,"PS5 mouse ABI");
#endif
