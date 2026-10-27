/* SPDX-License-Identifier: GPL-3.0-or-later
 * Adapt the existing model's 1080p layout to the upstream SDF kit.
 */
#pragma once
#include "toolkit_surface.hpp"
#include "branding_logo.hpp"
#include <array>
#include <atomic>
namespace prospero_ui {
inline Surface* surface=nullptr;
inline std::atomic<bool> healthy{true};
inline bool motion=false,reduced=false;
inline float dt=1.0f/60;
inline std::array<hui::ui::PushButton,16>* buttons=nullptr;
inline unsigned button_index=0;
inline hui::gfx::Color color(std::uint32_t c){return {float(c&255)/255,float((c>>8)&255)/255,float((c>>16)&255)/255,float((c>>24)&255)/255};}
inline hui::ui::Theme theme(){auto t=hui::ui::default_theme();t.style=hui::ui::SurfaceStyle::soft;t.page=hui::gfx::Color::rgb(0x081a13);t.surface=hui::gfx::Color::rgb(0x132d22);t.primary=hui::gfx::Color::rgb(0xb6f2be);t.on_primary=hui::gfx::Color::rgb(0x102c1b);t.secondary=hui::gfx::Color::rgb(0x244438);t.on_secondary=t.text=hui::gfx::Color::rgb(0xeaf0e8);t.focus=hui::gfx::Color::rgb(0xa9eab6);t.radius=18;t.shadow_blur=16;t.focus_width=2;t.omega=22;t.damping=1;return t;}
struct Canvas {
 void gradient(std::uint32_t a,std::uint32_t b){surface->list.gradient_rect({0,0,1920,1080},0,color(a),color(b));button_index=0;motion=false;}
 void rounded(int x,int y,unsigned w,unsigned h,unsigned r,std::uint32_t c){surface->list.rounded_rect({float(x),float(y),float(w),float(h)},float(r),color(c));}
 void rectangle(unsigned x,unsigned y,unsigned w,unsigned h,ps5::demo::Color c){rounded(int(x),int(y),w,h,0,static_cast<std::uint32_t>(c));}
 void disc(int x,int y,unsigned r,std::uint32_t c){surface->list.circle(float(x),float(y),float(r),color(c));}
 void label(int x,int y,std::string_view value,unsigned size,std::uint32_t c){auto& face=size>=30?surface->fonts.semibold:surface->fonts.regular;hui::ui::text(surface->list,face,value,float(x),float(y)+face.font->ascent(float(size)),float(size),color(c));}
 static unsigned text_width(std::string_view value,unsigned size){auto& face=size>=30?surface->fonts.semibold:surface->fonts.regular;return unsigned(face.measure(value,float(size))+0.5f);}
 void logo(int x,int y,int size){surface->list.image(surface->logo,{float(x),float(y),float(size),float(size)},{0,0,1,1},hui::gfx::Color::rgb(0xffffff),0);}
 void button(int x,int y,int w,int h,const char* text,bool active,bool primary,bool press=false){
  if(button_index>=buttons->size())return;auto& b=(*buttons)[button_index++];b.style.theme=theme();b.style.height=float(h);b.style.text_size=30;b.style.reduced_motion=reduced;b.style.press_scale=reduced?0:0.018f;b.style.role=primary?(std::string_view(text)=="DELETE INSTANCE"?hui::ui::ButtonRole::danger:hui::ui::ButtonRole::primary):hui::ui::ButtonRole::secondary;b.label=text;b.set_bounds({float(x),float(y),float(w),float(h)});b.set_active(active);if(active&&press)b.press();b.update(dt);hui::ui::Canvas c{surface->list,surface->fonts};b.draw(c);
 }
};
inline bool open(const char* fonts){
 if(surface)return healthy;
 surface=new Surface;buttons=new std::array<hui::ui::PushButton,16>;healthy=surface->init(fonts);
 if(healthy){std::array<std::uint32_t,72*72> pixels{};for(unsigned i=0;i<pixels.size();i++)pixels[i]=prospero_menu::logo_pixels[i];surface->logo=surface->renderer.create_texture(72,72,reinterpret_cast<const std::uint8_t*>(pixels.data()));healthy=surface->logo!=0;}
 std::fprintf(stderr,"PS5_UI Vulkan init=%s stage=%s result=%d\n",healthy?"READY":"FAIL",surface->stage,int(surface->error));
 return healthy;
}
inline bool close(){if(!surface)return healthy;bool result=surface->close();if(result){delete buttons;buttons=nullptr;delete surface;surface=nullptr;}return healthy&&result;}
}
