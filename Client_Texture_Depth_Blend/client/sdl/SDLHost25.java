import java.nio.*;
import org.lwjgl.system.*;
import org.lwjgl.sdl.*;
import static org.lwjgl.sdl.SDLInit.*;
import static org.lwjgl.sdl.SDLError.*;
import static org.lwjgl.sdl.SDLJoystick.*;
import static org.lwjgl.sdl.SDLGamepad.*;
import static org.lwjgl.sdl.SDLEvents.*;
import static org.lwjgl.sdl.SDLHints.*;
public final class SDLHost25 {
 static native int attachVirtual();
 static void check(boolean result,String call){if(!result)throw new AssertionError(call+": "+SDL_GetError());}
 public static void main(String[] args){
  System.load(args[0]);Configuration.MEMORY_ALLOCATOR.set("system");Configuration.SDL_LIBRARY_NAME.set(args[1]);Library.initialize();
  check(SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS,"1"),"background input hint");
  check(SDL_Init(SDL_INIT_GAMEPAD),"SDL_Init GAMEPAD");
  try(MemoryStack stack=MemoryStack.stackPush()) {
   int id=attachVirtual();if(id==0)throw new AssertionError("attach virtual: "+SDL_GetError());
   if(!SDL_IsGamepad(id))throw new AssertionError("Virtual gamepad mapping");long pad=SDL_OpenGamepad(id);if(pad==0)throw new AssertionError("open gamepad: "+SDL_GetError());long joystick=SDL_GetGamepadJoystick(pad);
   try(SDL_Event event=SDL_Event.calloc()) {
    while(SDL_PollEvent(event)){}
    check(SDL_SetJoystickVirtualButton(joystick,SDL_GAMEPAD_BUTTON_SOUTH,true),"virtual SOUTH");check(SDL_SetJoystickVirtualAxis(joystick,SDL_GAMEPAD_AXIS_LEFTX,(short)24576),"virtual LEFTX");SDL_UpdateJoysticks();
    if(!SDL_GetGamepadButton(pad,SDL_GAMEPAD_BUTTON_SOUTH)||SDL_GetGamepadAxis(pad,SDL_GAMEPAD_AXIS_LEFTX)<20000)throw new AssertionError("Gamepad state via original bindings");
    boolean down=false,axis=false;while(SDL_PollEvent(event)){if(event.type()==SDL_EVENT_GAMEPAD_BUTTON_DOWN&&event.gbutton().button()==SDL_GAMEPAD_BUTTON_SOUTH)down=true;if(event.type()==SDL_EVENT_GAMEPAD_AXIS_MOTION&&event.gaxis().axis()==SDL_GAMEPAD_AXIS_LEFTX&&event.gaxis().value()>20000)axis=true;}
    if(!down||!axis)throw new AssertionError("SDL_Event button/axis ABI");
    check(SDL_SetJoystickVirtualButton(joystick,SDL_GAMEPAD_BUTTON_SOUTH,false),"virtual release");SDL_UpdateJoysticks();if(SDL_GetGamepadButton(pad,SDL_GAMEPAD_BUTTON_SOUTH))throw new AssertionError("release state");
   } finally {SDL_CloseGamepad(pad);check(SDL_DetachVirtualJoystick(id),"detach virtual");}
   System.out.println("PASS original SDL Java bindings with real host SDL3: version"+SDLVersion.SDL_GetVersion()+", gamepad state, button/axis events, struct ABI, release and cleanup. Host virtual input only; no PS5 driver/window/display validation.");
  }finally{SDL_Quit();}
 }
}
